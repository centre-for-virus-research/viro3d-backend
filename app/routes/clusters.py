from natsort import natsorted
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_clusters_collection
from app.models.clusters import *

router = APIRouter(
    prefix="/clusters",
    tags=["clusters"],
    responses={404: {"description": "Not Found"}},
)

@router.get('/genbank_id/', include_in_schema=True, response_model=dict)
async def get_cluster_by_genbank_id(qualifier: str, db: AsyncIOMotorDatabase = Depends(get_clusters_collection)):
    """
    Get Cluster of Similar Protein Structures by Genbank ID
    """

    results = []

    similar_structs = db.find({"cluster_members.member_record_id": { '$regex' : qualifier }})

    async for row in similar_structs:
        results.append(row)

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="No Similar Structures Found")
    
    else:

        result = ClusterResult(
            genbank_id = qualifier,
            clusters = results).model_dump(by_alias=False
        )

        return result