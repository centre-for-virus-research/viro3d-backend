from operator import itemgetter
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
import natsort
from app.db import get_genome_coordinates_collection
from app.models.genome_coordinates import *

router = APIRouter(
    prefix="/genome_coordinates",
    tags=["Genome_coordinates"],
    responses={404: {"description": "Not Found"}},
)

@router.get('/virus_name/', include_in_schema=False, response_model=dict)
async def get_genome_coordinates_by_virus_name(qualifier: str, db: AsyncIOMotorDatabase = Depends(get_genome_coordinates_collection)):
    """
    List Genome Coordinates by virus name
    """
    query = {
        "coordinates": {
            "$elemMatch": {
                "virus_name": qualifier
            }
        }
    }
    cursor = db.aggregate([
        {"$match": query}
    ])
    
    results = await cursor.to_list(length=None)
    
    if not results:
        raise HTTPException(status_code=404, detail="No Coordinates Found")

    segments = [
        GenomeCoordinatesEntry(**row) for row in natsort.natsorted(results, key=itemgetter('segment'))
    ]

    return GenomeSegmentsEntry(
        qualifier=qualifier,
        segments=segments).model_dump(by_alias=False
) 

