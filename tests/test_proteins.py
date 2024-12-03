from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from mongomock_motor import AsyncMongoMockClient
from app.db import get_protein_structures_collection
from app.main import app
from app.models.proteins import *

@pytest.mark.asyncio
async def test_get_protein_structures_by_record_id(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)
    
    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/recordid/CAI74981.1.4_11505"
    )

    protein_fetched: RecordIDEntry = RecordIDEntry(**response.json())
    
    expected_response = RecordIDEntry(record_id='CAI74981.1.4_11505', protein_structure=ProteinStructure(record_id='CAI74981.1.4_11505', uniprot_id='Q2PBR5', pept_cat='mat_pept', protlen=13, genbank_name_curated='Pep13 protein', gene='', product='polyprotein precursor', note='pep13 protein', genbank_id='CAI74981.1', mat_pept_id='CAI74981.1.4', reg_id='', uniq_id='CAI74981.1.4', uniprot_match_status='protein_substring', nt_acc='AJ920335.1', acc='AJ920335', seg='SegA', taxid=321302, Sort=11505, Realm='Riboviria', Subrealm='', Kingdom='Orthornavirae', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Birnaviridae', Subfamily='', Genus='Telnavirus', Subgenus='', Species='Telnavirus tellinae', Exemplar_or_additional_isolate='E', Virus_name_s_='Tellina virus 1', Virus_name_abbreviation_s_='TV1', Virus_isolate_designation='', Virus_REFSEQ_accession='SegA: NC_038869; SegB: NC_038870', Genome_coverage='Complete genome', Genome_composition='dsRNA', Host_source='invertebrates', host='Tellina tenuis', genbank_genome_coordinates='[1595:1633](+)', genome_coordinates='[1594:1633](+)', protein_coordinates='[499:512]', esmfold_log_pLDDT='61.3', esmfold_log_pTM='0.011', colabfold_json_pLDDT='71.8', colabfold_json_pTM='0.03', PC1='-88.78831333582852', PC2='41.31979190633098', PC3='45.31532770748655', protein_seq='ASGKPLYRNMALA', structure_seq='ASGKPLYRNMALA', genome_length_bp=3579.0))
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()