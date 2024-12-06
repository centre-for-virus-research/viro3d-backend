from app.utils.env_variables import BLAST_DB_PATH
from app.utils.helpers import calculate_match_score, validate_regex
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_protein_structures_collection
from app.models.proteins import *
from Bio.Blast.Applications import NcbiblastpCommandline
from io import StringIO
from Bio.Blast import NCBIXML

router = APIRouter(
    prefix="/proteins",
    tags=["Protein Structures"],
    responses={404: {"description": "Not Found"}},
)

@router.get('/recordid/{qualifier}', include_in_schema=False, response_model=dict)
async def get_protein_structures_by_record_id(qualifier: str, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    """
    Find a protein structure by its record_id
    """

    structure = await db.find_one({ "_id": qualifier })

    if not structure:
        raise HTTPException(status_code=404, detail="No Structures Found")
    
    else:

        result = RecordIDEntry(
            record_id = qualifier,
            protein_structure = structure).model_dump(by_alias=False
        )

        return result

@router.get('/proteinname/', response_model=dict)
async def get_protein_structures_by_protein_name(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    """
    List Protein Structures by Protein Name
    """

    skips = 0
    if page_size and page_num:
        skips = page_size * (page_num - 1)

    qualifier = validate_regex(qualifier)
    
    query = { "genbank_name_curated": { '$regex' : qualifier, '$options' : 'i' } }
    cursor = db.find(query)

    results = await cursor.to_list(length=None)
    
    sorted_results = sorted(
        results, 
        key=lambda x: calculate_match_score(x['genbank_name_curated'], qualifier),
        reverse=True
    )

    paginated_results = sorted_results[skips:skips + page_size] if page_size else sorted_results
    
    if not paginated_results:
        raise HTTPException(status_code=404, detail="No Structures Found")

    return ProteinNameEntry(
        proteinname = qualifier,
        count = len(results),
        protein_structures = paginated_results).model_dump(by_alias=False
    )

@router.get('/genbankid/', response_model=dict)
async def get_protein_structures_by_genbank_id(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    """
    List Protein Structures by Genbank ID
    """

    skips = 0
    if page_size and page_num:
        skips = page_size * (page_num - 1)
    
    query = { "protein_id": {'$regex': qualifier, '$options' : 'i'} }
    cursor = db.find(query).skip(skips).limit(page_size) if page_size else db.find(query)

    results = await cursor.to_list(length=page_size)

    if not results:
        raise HTTPException(status_code=404, detail="No Structures Found")
    
    count = await db.count_documents(query)

    return GenbankEntry(
        genbank_id = qualifier,
        count = count,
        protein_structures = results).model_dump(by_alias=False
)
        
@router.get('/virus_name/', response_model=dict)
async def get_protein_structures_by_virus_name(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):

    """
    List Protein Structures by Virus Name
    """

    skips = 0
    if page_size and page_num:
        skips = page_size * (page_num - 1)
    
    qualifier = validate_regex(qualifier)
    query = { "$or": [ { "Virus name(s)": { "$regex": qualifier, "$options": "i" } }, { "Virus name abbreviation(s)": { "$regex": qualifier, "$options": "i" } }] }
    cursor = db.find(query).skip(skips).limit(page_size) if page_size else db.find(query)

    results = await cursor.to_list(length=page_size)

    if not results:
        raise HTTPException(status_code=404, detail="No Structures Found")
    
    count = await db.count_documents(query)

    return VirusEntry(
        virus_name = qualifier,
        count = count,
        protein_structures = results).model_dump(by_alias=False
    )

#This route is used when the user clicks a suggestion in the autocomplete menu when searching by virus name - it is hidden in the API spec
@router.get('/virus_name/', include_in_schema=False, response_model=dict)
async def get_protein_structures_by_exact_virus_name(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):

    """
    List Protein Structures by querying with the exact Virus Name
    """

    skips = 0
    if page_size and page_num:
        skips = page_size * (page_num - 1)
    
    query = { "Virus name(s)":  qualifier }
  
    cursor = db.find(query).skip(skips).limit(page_size) if page_size else db.find(query)

    results = await cursor.to_list(length=page_size)

    if not results:
        raise HTTPException(status_code=404, detail="No Structures Found")
    
    count = await db.count_documents(query)

    return VirusEntry(
        virus_name = qualifier,
        count = count,
        protein_structures = results).model_dump(by_alias=False
    )

@router.get('/sequencematch/', response_model=dict)
async def get_protein_structures_by_sequence(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    """
    List Protein Structures by blastp sequence match
    """
    
    skips = 0
    if page_size and page_num:
        skips = page_size * (page_num - 1)

    if not (qualifier.isalpha() and ' ' not in qualifier):
        raise HTTPException(status_code=400, detail="Search term contains non-alphabetic characters and/or spaces. Please re-enter your sequence")

    #viro3d_blast_db is the name of the blast database - it just automatically names it after the .fas file unless specifed
    
    blastp_cline = NcbiblastpCommandline(db=BLAST_DB_PATH, outfmt=5, num_threads=4) 
    
    stdout, stderr = blastp_cline(stdin=qualifier.upper(), stdout=True, stderr=True)
    
    if stderr:
        print(f"Error occurred: {stderr}")
    
    result_handle = StringIO(stdout)
    blast_records = NCBIXML.parse(result_handle)

    results = []
        
    for record in blast_records:
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                structure = await db.find_one({ "_id": alignment.hit_def })
                match = BlastMatch(
                    structure_id = alignment.hit_def,
                    score = hsp.score,
                    evalue = hsp.expect,
                    hit_length = alignment.length,
                    positives = hsp.positives,
                    gaps = hsp.gaps,
                    protein_structure = structure
                )

                results.append(match)

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="No Matches Found")
    
    else:
        
        results = sorted(
            results,
            key=lambda match: match.evalue,
            )
        
        paginated_results = results[skips:skips + page_size] if page_size else results
        
        result = BlastEntry(
            sequence = qualifier.upper(),
            matches = paginated_results).model_dump(by_alias=False
        )

        return result