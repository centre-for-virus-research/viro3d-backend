from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_protein_structures_collection
from app.models.proteins import *

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