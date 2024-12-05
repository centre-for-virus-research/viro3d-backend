from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.db import get_protein_structures_collection
from app.main import app
from app.models.viruses import *

@pytest.mark.asyncio
async def test_get_viruses_by_virus_name(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/viruses/?qualifier=gyrovirus 4"
    )
    
    protein_fetched: VirusName = VirusName(**response.json())
    
    expected_response = VirusName(search_term='gyrovirus 4', count=1, viruses=[{'_id': 'gyrovirus 4'}])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_viruses_by_virus_abbreviation(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/viruses/?qualifier=GyV4"
    )
    
    protein_fetched: VirusName = VirusName(**response.json())
    
    expected_response = VirusName(search_term='GyV4', count=1, viruses=[{'_id': 'gyrovirus 4'}])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_viruses_by_virus_species(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/viruses/?qualifier=Gyrovirus homsa3"
    )
    
    protein_fetched: VirusName = VirusName(**response.json())
    
    expected_response = VirusName(search_term='Gyrovirus homsa3', count=1, viruses=[{'_id': 'gyrovirus 4'}])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_viruses_with_substring(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/viruses/?qualifier=gyrovirus"
    )
    
    protein_fetched: VirusName = VirusName(**response.json())
    
    expected_response = VirusName(search_term='gyrovirus', count=3, viruses=[{'_id': 'gyrovirus 4'}, {'_id': 'gyrovirus 11'}, {'_id': 'avian gyrovirus 2'}])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_viruses_no_matches(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/viruses/?qualifier=no_match"
    )
    
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Matches Found"}
    app.dependency_overrides.clear()