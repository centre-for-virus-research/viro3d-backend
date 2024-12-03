import pytest
import json

@pytest.fixture
def mock_protein_data():
    with open("./mock_data/test_protein_structures.json") as f:
        return json.load(f)
    
    