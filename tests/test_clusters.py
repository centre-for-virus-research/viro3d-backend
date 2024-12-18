from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.db import get_clusters_collection
from app.main import app
from app.models.clusters import *

@pytest.mark.asyncio
async def test_get_cluster_by_genbank_id(mock_clusters_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["clusters"]
    await mock_collection.insert_many(mock_clusters_data)

    app.dependency_overrides[get_clusters_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/clusters/genbank_id/?qualifier=AFU07689.1"
    )
    clusters_fetched: ClusterResult = ClusterResult(**response.json())
    
    expected_response = ClusterResult(genbank_id='AFU07689.1', clusters=[Cluster(cluster_representative='CF-AFU07689.1_4668_relaxed', cluster_members=[ClusterMember(cluster_rep_id='CF-AFU07689.1_4668_relaxed', member_record_id='AFU07689.1_4668', protein_length=146, tax_id=1235430, species='Dyorhopapillomavirus 1', plDDT_score=84.9, virus_name='Equus caballus papillomavirus 7', family='Papillomaviridae', host='Equus ferus caballus', genbank_name_curated='Product: putative E6 protein', uniprot_id='M4HXD6', genbank_id='AFU07689.1', nucleotide_accession_number='JX035935.1'), ClusterMember(cluster_rep_id='CF-AFU07689.1_4668_relaxed', member_record_id='ADV03081.1_4646', protein_length=150, tax_id=940834, species='Dyoiotapapillomavirus 1', plDDT_score=87.6, virus_name='Equus caballus papillomavirus 3', family='Papillomaviridae', host='Equus caballus', genbank_name_curated='Product: putative E6 early protein', uniprot_id='E7C0H0', genbank_id='ADV03081.1', nucleotide_accession_number='GU384895.1')])])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert clusters_fetched == expected_response

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_cluster_by_genbank_id_no_match(mock_clusters_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["clusters"]
    await mock_collection.insert_many(mock_clusters_data)

    app.dependency_overrides[get_clusters_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/clusters/genbank_id/?qualifier=no_match"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Similar Structures Found"}
    app.dependency_overrides.clear()