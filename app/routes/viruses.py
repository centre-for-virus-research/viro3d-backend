from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_protein_structures_collection
from app.models.viruses import *
from app.utils.helpers import validate_regex, calculate_match_score

router = APIRouter(
    prefix="/viruses",
    tags=["Viruses"],
    responses={404: {"description": "Not Found"}},
)

@router.get('/', include_in_schema=False, response_model=dict)
async def get_viruses(qualifier: str, page_size: int = None, page_num: int = None, db: AsyncIOMotorDatabase = Depends(get_protein_structures_collection)):
    """
    List Viruses present in the data set, sorted by match relevance
    """

    skips = page_size * (page_num - 1) if page_size and page_num else 0
    
    qualifier = validate_regex(qualifier)

    virus_query = { 
        "$or": [
            {"Virus name(s)": {"$regex": qualifier, "$options": "i"}},
            {"Virus name abbreviation(s)": {"$regex": qualifier, "$options": "i"}},
            {"Species": {"$regex": qualifier, "$options": "i"}}
        ]
    }
    
    virus_cursor = db.aggregate([
        {"$match": virus_query},
        {"$group": {"_id": "$Virus name(s)"}},
    ])
    
    virus_name_results = await virus_cursor.to_list(length=None) 
    
    # Sort results by relevance based on the calculated score
    sorted_results = sorted(
        virus_name_results, 
        key=lambda x: calculate_match_score(x['_id'], qualifier),
        reverse=True
    )
    
    paginated_results = sorted_results[skips:skips + page_size] if page_size else sorted_results

    if not paginated_results:
        raise HTTPException(status_code=404, detail="No Matches Found")
    
    return VirusName(
        search_term=qualifier,
        count = len(sorted_results),
        viruses=paginated_results).model_dump(by_alias=False
    )