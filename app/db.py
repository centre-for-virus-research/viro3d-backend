from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.env_variables import CONNECTION_STRING

def get_protein_structures_collection():
    client = AsyncIOMotorClient(CONNECTION_STRING)
    try:
        yield client.viro3dtreetest.get_collection("proteinstructures")
    finally:
        client.close()