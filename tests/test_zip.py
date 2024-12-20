from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.db import get_protein_structures_collection
from app.main import app
from io import BytesIO
import zipfile

@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_strucure_IDs_cif(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/virus/gyrovirus 4/.cif"
    )
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    
    zip_buffer = BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files_in_zip = zip_file.namelist()
        
        metadata_csv = "gyrovirus 4_metadata.csv"
        assert metadata_csv in files_in_zip, f"{metadata_csv} not found in the zip"
        
        expected_files = ["CF-AFO67214.1_12633.cif", "CF-AFO67213.1_12633.cif"]
        for expected_file in expected_files:
            assert expected_file in files_in_zip, f"{expected_file} not found in the zip"
        
        with zip_file.open(metadata_csv) as csv_file:
            csv_content = csv_file.read().decode("utf-8")
            rows = csv_content.splitlines()
            headers = rows[0].split(",")
            
            expected_csv_headers = [
                "record_id",
                "protein_name",
                "virus_name",
                "species",
                "family",
                "host",
                "protein_length (No. of Residues)",
                "uniprot_id",
                "genbank_id",
                "taxid",
                "nucleotide_accession_number",
                "ESMFold pLDDT Score",
                "ColabFold pLDDT Score"
            ]
            assert headers == expected_csv_headers, f'CSV headers mismatch: {headers}'
            
            assert len(rows) > 1, "CSV file is empty except for the header"
    
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_strucure_IDs_pdb(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/virus/gyrovirus 4/_relaxed.pdb"
    )
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    
    zip_buffer = BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files_in_zip = zip_file.namelist()
        
        metadata_csv = "gyrovirus 4_metadata.csv"
        assert metadata_csv in files_in_zip, f"{metadata_csv} not found in the zip"
        
        expected_files = ["CF-AFO67214.1_12633_relaxed.pdb", "CF-AFO67213.1_12633_relaxed.pdb"]
        for expected_file in expected_files:
            assert expected_file in files_in_zip, f"{expected_file} not found in the zip"
        
        with zip_file.open(metadata_csv) as csv_file:
            csv_content = csv_file.read().decode("utf-8")
            rows = csv_content.splitlines()
            headers = rows[0].split(",")
            
            expected_csv_headers = [
                "record_id",
                "protein_name",
                "virus_name",
                "species",
                "family",
                "host",
                "protein_length (No. of Residues)",
                "uniprot_id",
                "genbank_id",
                "taxid",
                "nucleotide_accession_number",
                "ESMFold pLDDT Score",
                "ColabFold pLDDT Score"
            ]
            assert headers == expected_csv_headers, f'CSV headers mismatch: {headers}'
            
            assert len(rows) > 1, "CSV file is empty except for the header"
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_strucure_IDs_wrong_format_argument(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/virus/gyrovirus 4/.pdf"
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "The file extension provided is not available"}

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_strucure_IDs_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/virus/no_match/.pdb"
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "The file extension provided is not available"}

    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_cluster_ID_cif(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/cluster/CF-AFU07689.1_4668_relaxed/.cif"
    )
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    
    zip_buffer = BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files_in_zip = zip_file.namelist()
        
        metadata_csv = "CF-AFU07689.1_4668_relaxed_metadata.csv"
        assert metadata_csv in files_in_zip, f"{metadata_csv} not found in the zip"
        
        expected_files = ["CF-ADV03081.1_4646.cif", "CF-AFU07689.1_4668.cif"]
        for expected_file in expected_files:
            assert expected_file in files_in_zip, f"{expected_file} not found in the zip"
        
        with zip_file.open(metadata_csv) as csv_file:
            csv_content = csv_file.read().decode("utf-8")
            rows = csv_content.splitlines()
            headers = rows[0].split(",")
            
            expected_csv_headers = [
                "record_id",
                "protein_name",
                "virus_name",
                "species",
                "family",
                "host",
                "protein_length (No. of Residues)",
                "uniprot_id",
                "genbank_id",
                "taxid",
                "nucleotide_accession_number"
            ]
            assert headers == expected_csv_headers, f'CSV headers mismatch: {headers}'
            
            assert len(rows) > 1, "CSV file is empty except for the header"
    
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_cluster_ID_pdb(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/cluster/CF-AFU07689.1_4668_relaxed/_relaxed.pdb"
    )
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    
    zip_buffer = BytesIO(response.content)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        files_in_zip = zip_file.namelist()
        
        metadata_csv = "CF-AFU07689.1_4668_relaxed_metadata.csv"
        assert metadata_csv in files_in_zip, f"{metadata_csv} not found in the zip"
        
        expected_files = ["CF-ADV03081.1_4646_relaxed.pdb", "CF-AFU07689.1_4668_relaxed.pdb"]
        for expected_file in expected_files:
            assert expected_file in files_in_zip, f"{expected_file} not found in the zip"
        
        with zip_file.open(metadata_csv) as csv_file:
            csv_content = csv_file.read().decode("utf-8")
            rows = csv_content.splitlines()
            headers = rows[0].split(",")
            
            expected_csv_headers = [
                "record_id",
                "protein_name",
                "virus_name",
                "species",
                "family",
                "host",
                "protein_length (No. of Residues)",
                "uniprot_id",
                "genbank_id",
                "taxid",
                "nucleotide_accession_number"
            ]
            assert headers == expected_csv_headers, f'CSV headers mismatch: {headers}'
            
            assert len(rows) > 1, "CSV file is empty except for the header"
    
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_cluster_ID_wrong_format_argument(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/cluster/CF-AFU07689.1_4668_relaxed/.pdf"
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "The file extension provided is not available"}

    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_structural_models_Zip_by_cluster_ID_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/zip/cluster/no_match/.pdb"
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "The file extension provided is not available"}

    app.dependency_overrides.clear()