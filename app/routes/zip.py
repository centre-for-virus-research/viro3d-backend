from app.utils.env_variables import STRUCTURAL_MODELS_PATH
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_clusters_collection, get_protein_structures_collection
import csv
from io import BytesIO, StringIO
import os
import zipfile
from .limiter import limiter

router = APIRouter(
    prefix="/zip",
    tags=["Zip"],
    responses={404: {"description": "Not Found"}},
)

@router.get('/virus/{qualifier}/{format}', include_in_schema=False)
@limiter.limit("3/minute")
async def get_structural_models_Zip_by_strucure_IDs(request: Request, qualifier: str, format: str, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    
    if format not in [".cif", "_relaxed.pdb"]:
        raise HTTPException(status_code=400, detail="The file extension provided is not available")

    query = {"Virus name(s)": qualifier}
    cursor = db.find(query)

    json = await cursor.to_list(length=None)

    if not json:
        raise HTTPException(status_code=404, detail="No Models Found")
    
    results = []
    csvfile = []
    
    for row in json:
        csvfile.append({
            'record_id': row['_id'],
            'protein_name': row['genbank_name_curated'],
            'virus_name': row['Virus name(s)'],
            'species': row['Species'],
            'family': row['Family'],
            'host': row['host'],
            'protein_length (No. of Residues)': row['protlen'],
            'uniprot_id': row['uniprot_id'],
            'genbank_id': row['protein_id'],
            'taxid': row['taxid'],
            'nucleotide_accession_number': row['nt_acc'],
            'ESMFold pLDDT Score': row['esmfold_log_pLDDT'],
            'ColabFold pLDDT Score': row['colabfold_json_pLDDT']
        })
        results.append(row['_id'])

    # Create CSV object
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write CSV header and rows
    header_written = False
    for record in csvfile:
        if not header_written:
            csv_writer.writerow(record.keys())  # Write headers
            header_written = True
        csv_writer.writerow(record.values())  # Write each row
    
    # Reset buffer position to start
    csv_buffer.seek(0)
    
    # Create the zip file in memory
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        
        # Add the CSV file to the zip
        zf.writestr(f'{qualifier}_metadata.csv', csv_buffer.getvalue())
        
        # Add each PDB file to the zip
        for id in results:
            path = f'{STRUCTURAL_MODELS_PATH}EF-{id}{format}'
            if os.path.exists(path):
                zf.write(f'{STRUCTURAL_MODELS_PATH}EF-{id}{format}', arcname=f'EF-{id}{format}')
            zf.write(f'{STRUCTURAL_MODELS_PATH}CF-{id}{format}', arcname=f'CF-{id}{format}')
         
    # Prepare zip for streaming response
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={qualifier}_{format}.zip"},
    )

@router.get('/cluster/{qualifier}/{format}', include_in_schema=False)
@limiter.limit("3/minute")
async def get_structural_models_Zip_by_cluster_ID(request: Request, qualifier: str, format: str, db: AsyncIOMotorDatabase = Depends(get_clusters_collection)):
    
    if format not in [".cif", "_relaxed.pdb"]:
        raise HTTPException(status_code=400, detail="The file extension provided is not available")

    json = await db.find_one({ "_id": qualifier })
    
    print(json)

    if not json:
        raise HTTPException(status_code=404, detail="No Models Found")
    
    results = []
    csvfile = []
    
    for row in json['cluster_members']:
        csvfile.append({
            'record_id': row['member_record_id'],
            'protein_name': row['genbank_name_curated'],
            'virus_name': row['virus_name'],
            'species': row['species'],
            'family': row['family'],
            'host': row['host'],
            'protein_length (No. of Residues)': row['protein_length'],
            'uniprot_id': row['uniprot_id'],
            'genbank_id': row['genbank_id'],
            'taxid': row['tax_id'],
            'nucleotide_accession_number': row['nucleotide_accession_number']
        })
        
        results.append(row['member_record_id'])

    # Create CSV object
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    
    # Write CSV header and rows
    header_written = False
    for record in csvfile:
        if not header_written:
            csv_writer.writerow(record.keys())  # Write headers
            header_written = True
        csv_writer.writerow(record.values())  # Write each row
    
    # Reset buffer position to start
    csv_buffer.seek(0)
    
    # Create the zip file in memory
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        
        # Add the CSV file to the zip
        zf.writestr(f'{qualifier}_metadata.csv', csv_buffer.getvalue())
        
        # Add each PDB file to the zip
        for member_record_id in results:
            path = f'{STRUCTURAL_MODELS_PATH}EF-{member_record_id}{format}'
            if os.path.exists(path):
                zf.write(f'{STRUCTURAL_MODELS_PATH}EF-{member_record_id}{format}', arcname=f'EF-{member_record_id}{format}')
            zf.write(f'{STRUCTURAL_MODELS_PATH}CF-{member_record_id}{format}', arcname=f'CF-{member_record_id}{format}')
         
    # Prepare zip for streaming response
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={qualifier}_{format}.zip"},
    )