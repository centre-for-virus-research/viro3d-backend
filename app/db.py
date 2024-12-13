from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.env_variables import CONNECTION_STRING

def get_protein_structures_collection():
    client = AsyncIOMotorClient(CONNECTION_STRING)
    try:
        yield client.viro3d.get_collection("proteinstructures")
    finally:
        client.close()

def get_genome_coordinates_collection():
    client = AsyncIOMotorClient(CONNECTION_STRING)
    try:
        yield client.viro3d.get_collection("genome_coordinates")
    finally:
        client.close()

def get_clusters_collection():
    client = AsyncIOMotorClient(CONNECTION_STRING)
    try:
        yield client.viro3d.get_collection("clusters")
    finally:
        client.close()