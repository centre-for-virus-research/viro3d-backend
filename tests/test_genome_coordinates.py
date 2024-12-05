from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.db import get_genome_coordinates_collection
from app.main import app
from app.models.genome_coordinates import *

@pytest.mark.asyncio
async def test_get_genome_coordinates_by_virus_name(mock_genome_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["genome_coordinates"]
    await mock_collection.insert_many(mock_genome_data)

    app.dependency_overrides[get_genome_coordinates_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/genome_coordinates/virus_name/?qualifier=ovine adenovirus 3"
    )
    coordinates_fetched: GenomeSegmentsEntry = GenomeSegmentsEntry(**response.json())
    
    expected_response = GenomeSegmentsEntry(qualifier='ovine adenovirus 3', segments=[GenomeCoordinatesEntry(nt_acc='DQ630756.1', segment='Non-segmented', genome_length_bp=2727.0, isolate_designation='PX611', coordinates=[GenomeCoordinates(id='ABG22142.1_12249', nt_acc='DQ630756.1', virus_name='ovine adenovirus 3', gene_name='Product: hexon', pept_cat='protein', segment='Non-segmented', start=1.0, end=2727.0, strand='+', family='ABG22142.1_12249', join='none')])])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert coordinates_fetched == expected_response

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_genome_coordinates_by_virus_name_no_match(mock_genome_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["genome_coordinates"]
    await mock_collection.insert_many(mock_genome_data)

    app.dependency_overrides[get_genome_coordinates_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/genome_coordinates/virus_name/?qualifier=no_match"
    )
    
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Coordinates Found"}
    
    app.dependency_overrides.clear()
    