import pytest
import json

@pytest.fixture
def mock_protein_data():
    with open("./mock_data/test_protein_structures.json") as f:
        return json.load(f)

@pytest.fixture
def mock_genome_data():
    with open("./mock_data/test_genome_coordinates.json") as f:
        return json.load(f)
    