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


@pytest.mark.asyncio
async def test_get_protein_structures_by_record_id_no_match(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection
    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/recordid/no_match"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_get_protein_structures_by_protein_name(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/proteinname/?qualifier=Pep13 protein"
    )
    expected_response = ProteinNameEntry(proteinname='Pep13 protein', viruses=[{"_id": "Tellina virus 1"}], count=1, protein_structures=[ProteinStructure(record_id='CAI74981.1.4_11505', uniprot_id='Q2PBR5', pept_cat='mat_pept', protlen=13, genbank_name_curated='Pep13 protein', gene='', product='polyprotein precursor', note='pep13 protein', genbank_id='CAI74981.1', mat_pept_id='CAI74981.1.4', reg_id='', uniq_id='CAI74981.1.4', uniprot_match_status='protein_substring', nt_acc='AJ920335.1', acc='AJ920335', seg='SegA', taxid=321302, Sort=11505, Realm='Riboviria', Subrealm='', Kingdom='Orthornavirae', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Birnaviridae', Subfamily='', Genus='Telnavirus', Subgenus='', Species='Telnavirus tellinae', Exemplar_or_additional_isolate='E', Virus_name_s_='Tellina virus 1', Virus_name_abbreviation_s_='TV1', Virus_isolate_designation='', Virus_REFSEQ_accession='SegA: NC_038869; SegB: NC_038870', Genome_coverage='Complete genome', Genome_composition='dsRNA', Host_source='invertebrates', host='Tellina tenuis', genbank_genome_coordinates='[1595:1633](+)', genome_coordinates='[1594:1633](+)', protein_coordinates='[499:512]', esmfold_log_pLDDT='61.3', esmfold_log_pTM='0.011', colabfold_json_pLDDT='71.8', colabfold_json_pTM='0.03', PC1='-88.78831333582852', PC2='41.31979190633098', PC3='45.31532770748655', protein_seq='ASGKPLYRNMALA', structure_seq='ASGKPLYRNMALA', genome_length_bp=3579.0)])

    protein_fetched: ProteinNameEntry = ProteinNameEntry(**response.json())
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched== expected_response
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_protein_name_with_virus_filter(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/proteinname/?qualifier=Product: VP3&filter=avian gyrovirus 2"
    )
    expected_response = ProteinNameEntry(proteinname='Product: VP3', viruses=[{"_id": "avian gyrovirus 2"}], count=1, protein_structures=[ProteinStructure(record_id='AEB00703.1_12629', uniprot_id='F4ZDR1', pept_cat='protein', protlen=124, genbank_name_curated='Product: VP3', gene='', product='VP3', note='putative apoptosis function', genbank_id='AEB00703.1', mat_pept_id='', reg_id='', uniq_id='AEB00703.1', uniprot_match_status='match_protein_seq', nt_acc='HM590588.1', acc='HM590588', seg='', taxid=1002273, Sort=12629, Realm='', Subrealm='', Kingdom='', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Anelloviridae', Subfamily='', Genus='Gyrovirus', Subgenus='', Species='Gyrovirus galga1', Exemplar_or_additional_isolate='E', Virus_name_s_='avian gyrovirus 2', Virus_name_abbreviation_s_='AGyV2', Virus_isolate_designation='Ave 3', Virus_REFSEQ_accession='NC_015396', Genome_coverage='Complete genome', Genome_composition='ssDNA(-)', Host_source='vertebrates', host='Gallus gallus', genbank_genome_coordinates='[577:951](+)', genome_coordinates='[576:951](+)', protein_coordinates='', esmfold_log_pLDDT='30.7', esmfold_log_pTM='0.177', colabfold_json_pLDDT='53.2', colabfold_json_pTM='0.22', PC1='180.6665863282302', PC2='2.738125595180589', PC3='116.4085106988664', protein_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', structure_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', genome_length_bp=2383.0)])

    protein_fetched: ProteinNameEntry = ProteinNameEntry(**response.json())
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched== expected_response
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_protein_name_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response = await async_client.get(
        url=f"/proteins/proteinname/?qualifier=no_match"
    )

    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_protein_name_with_virus_filter_no_matches(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/proteinname/?qualifier=Product: VP3&filter=no_match"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_genbank_id(mock_protein_data):

    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/genbankid/?qualifier=AFO67214.1"
    )
    
    expected_response = GenbankEntry(genbank_id='AFO67214.1', count=1, protein_structures=[ProteinStructure(record_id='AFO67214.1_12633', uniprot_id='I7D351', pept_cat='protein', protlen=217, genbank_name_curated='Gene: VP2', gene='VP2', product='VP2', note='', genbank_id='AFO67214.1', mat_pept_id='', reg_id='', uniq_id='AFO67214.1', uniprot_match_status='match_protein_seq', nt_acc='JX310702.1', acc='JX310702', seg='', taxid=1214955, Sort=12633, Realm='', Subrealm='', Kingdom='', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Anelloviridae', Subfamily='', Genus='Gyrovirus', Subgenus='', Species='Gyrovirus homsa3', Exemplar_or_additional_isolate='E', Virus_name_s_='gyrovirus 4', Virus_name_abbreviation_s_='GyV4', Virus_isolate_designation='D137', Virus_REFSEQ_accession='NC_018401', Genome_coverage='Complete genome', Genome_composition='ssDNA(-)', Host_source='vertebrates', host='Homo sapiens', genbank_genome_coordinates='[518:1171](+)', genome_coordinates='[517:1171](+)', protein_coordinates='', esmfold_log_pLDDT='36.7', esmfold_log_pTM='0.135', colabfold_json_pLDDT='53.8', colabfold_json_pTM='0.26', PC1='65.34424355073803', PC2='-129.5251517589463', PC3='60.89868862883362', protein_seq='MGSPDHRFSAVPIDLLDSVCPQWKQVCFNYGIACWLTECRVSHSRVCRCTSFRNHWFQLEGKPVSTVEVGVQTDPGDLEPPRSGTSTAEIGPRVDAARRLLSSISFKRDACRALEGAPKPKKRKRGDARKEFLRRFREGEETESDAEWDSFVEWSDSDGDPGVDYMRGGAGGGILREDRMGGGIEVESTGGGTGGTEGTPFLKLLSGNFTSSTPARM', structure_seq='MGSPDHRFSAVPIDLLDSVCPQWKQVCFNYGIACWLTECRVSHSRVCRCTSFRNHWFQLEGKPVSTVEVGVQTDPGDLEPPRSGTSTAEIGPRVDAARRLLSSISFKRDACRALEGAPKPKKRKRGDARKEFLRRFREGEETESDAEWDSFVEWSDSDGDPGVDYMRGGAGGGILREDRMGGGIEVESTGGGTGGTEGTPFLKLLSGNFTSSTPARM', genome_length_bp=2034.0)])

    protein_fetched: GenbankEntry = GenbankEntry(**response.json())
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_genbank_id_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response = await async_client.get(
        url=f"/proteins/genbankid/?qualifier=no_match"
    )

    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_virus_name(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/virus_name/?qualifier=avian"
    )
    expected_response = VirusEntry(virus_name='avian', count=1, protein_structures=[ProteinStructure(record_id='AEB00703.1_12629', uniprot_id='F4ZDR1', pept_cat='protein', protlen=124, genbank_name_curated='Product: VP3', gene='', product='VP3', note='putative apoptosis function', genbank_id='AEB00703.1', mat_pept_id='', reg_id='', uniq_id='AEB00703.1', uniprot_match_status='match_protein_seq', nt_acc='HM590588.1', acc='HM590588', seg='', taxid=1002273, Sort=12629, Realm='', Subrealm='', Kingdom='', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Anelloviridae', Subfamily='', Genus='Gyrovirus', Subgenus='', Species='Gyrovirus galga1', Exemplar_or_additional_isolate='E', Virus_name_s_='avian gyrovirus 2', Virus_name_abbreviation_s_='AGyV2', Virus_isolate_designation='Ave 3', Virus_REFSEQ_accession='NC_015396', Genome_coverage='Complete genome', Genome_composition='ssDNA(-)', Host_source='vertebrates', host='Gallus gallus', genbank_genome_coordinates='[577:951](+)', genome_coordinates='[576:951](+)', protein_coordinates='', esmfold_log_pLDDT='30.7', esmfold_log_pTM='0.177', colabfold_json_pLDDT='53.2', colabfold_json_pTM='0.22', PC1='180.6665863282302', PC2='2.738125595180589', PC3='116.4085106988664', protein_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', structure_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', genome_length_bp=2383.0)])
    protein_fetched: VirusEntry = VirusEntry(**response.json())
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_virus_name_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/virus_name/?qualifier=no_match"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_exact_virus_name(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/virus_name/?qualifier=avian gyrovirus 2"
    )
    expected_response = VirusEntry(virus_name='avian gyrovirus 2', count=1, protein_structures=[ProteinStructure(record_id='AEB00703.1_12629', uniprot_id='F4ZDR1', pept_cat='protein', protlen=124, genbank_name_curated='Product: VP3', gene='', product='VP3', note='putative apoptosis function', genbank_id='AEB00703.1', mat_pept_id='', reg_id='', uniq_id='AEB00703.1', uniprot_match_status='match_protein_seq', nt_acc='HM590588.1', acc='HM590588', seg='', taxid=1002273, Sort=12629, Realm='', Subrealm='', Kingdom='', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Anelloviridae', Subfamily='', Genus='Gyrovirus', Subgenus='', Species='Gyrovirus galga1', Exemplar_or_additional_isolate='E', Virus_name_s_='avian gyrovirus 2', Virus_name_abbreviation_s_='AGyV2', Virus_isolate_designation='Ave 3', Virus_REFSEQ_accession='NC_015396', Genome_coverage='Complete genome', Genome_composition='ssDNA(-)', Host_source='vertebrates', host='Gallus gallus', genbank_genome_coordinates='[577:951](+)', genome_coordinates='[576:951](+)', protein_coordinates='', esmfold_log_pLDDT='30.7', esmfold_log_pTM='0.177', colabfold_json_pLDDT='53.2', colabfold_json_pTM='0.22', PC1='180.6665863282302', PC2='2.738125595180589', PC3='116.4085106988664', protein_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', structure_seq='MQTPRSRRQATTTRSELLTAYEHPTSSCPPAETTSIEIQIGIGSTIITLSLPGYASVRVLTTRSAPADDGGVTGSRRLADSSHRRPRRTSSPEIYVGFSAKERRQKENLITLREEGPPIKKLRL', genome_length_bp=2383.0)])
    protein_fetched: VirusEntry = VirusEntry(**response.json())
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_exact_virus_name_no_matches(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/virus_name/?qualifier=no_match"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Structures Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_sequence(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/sequencematch/?qualifier=ASGKPLYRNMALA"
    )
    protein_fetched: BlastEntry = BlastEntry(**response.json())
    
    expected_response = BlastEntry(sequence='ASGKPLYRNMALA', matches=[BlastMatch(structure_id='CAI74981.1.4_11505', score=63.0, evalue=0.00661371, hit_length=13, positives=13, gaps=0, protein_structure=ProteinStructure(record_id='CAI74981.1.4_11505', uniprot_id='Q2PBR5', pept_cat='mat_pept', protlen=13, genbank_name_curated='Pep13 protein', gene='', product='polyprotein precursor', note='pep13 protein', genbank_id='CAI74981.1', mat_pept_id='CAI74981.1.4', reg_id='', uniq_id='CAI74981.1.4', uniprot_match_status='protein_substring', nt_acc='AJ920335.1', acc='AJ920335', seg='SegA', taxid=321302, Sort=11505, Realm='Riboviria', Subrealm='', Kingdom='Orthornavirae', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Birnaviridae', Subfamily='', Genus='Telnavirus', Subgenus='', Species='Telnavirus tellinae', Exemplar_or_additional_isolate='E', Virus_name_s_='Tellina virus 1', Virus_name_abbreviation_s_='TV1', Virus_isolate_designation='', Virus_REFSEQ_accession='SegA: NC_038869; SegB: NC_038870', Genome_coverage='Complete genome', Genome_composition='dsRNA', Host_source='invertebrates', host='Tellina tenuis', genbank_genome_coordinates='[1595:1633](+)', genome_coordinates='[1594:1633](+)', protein_coordinates='[499:512]', esmfold_log_pLDDT='61.3', esmfold_log_pTM='0.011', colabfold_json_pLDDT='71.8', colabfold_json_pTM='0.03', PC1='-88.78831333582852', PC2='41.31979190633098', PC3='45.31532770748655', protein_seq='ASGKPLYRNMALA', structure_seq='ASGKPLYRNMALA', genome_length_bp=3579.0)), BlastMatch(structure_id='CAI74981.1_11505', score=66.0, evalue=0.0124488, hit_length=1114, positives=13, gaps=0, protein_structure=ProteinStructure(record_id='CAI74981.1_11505', uniprot_id='Q2PBR5', pept_cat='protein', protlen=1114, genbank_name_curated='Product: polyprotein precursor', gene='', product='polyprotein precursor', note='', genbank_id='CAI74981.1', mat_pept_id='', reg_id='', uniq_id='CAI74981.1', uniprot_match_status='match_protein_seq', nt_acc='AJ920335.1', acc='AJ920335', seg='SegA', taxid=321302, Sort=11505, Realm='Riboviria', Subrealm='', Kingdom='Orthornavirae', Subkingdom='', Phylum='', Subphylum='', Class='', Subclass='', Order='', Suborder='', Family='Birnaviridae', Subfamily='', Genus='Telnavirus', Subgenus='', Species='Telnavirus tellinae', Exemplar_or_additional_isolate='E', Virus_name_s_='Tellina virus 1', Virus_name_abbreviation_s_='TV1', Virus_isolate_designation='', Virus_REFSEQ_accession='SegA: NC_038869; SegB: NC_038870', Genome_coverage='Complete genome', Genome_composition='dsRNA', Host_source='invertebrates', host='Tellina tenuis', genbank_genome_coordinates='[98:3442](+)', genome_coordinates='[97:3442](+)', protein_coordinates='', esmfold_log_pLDDT='30.3', esmfold_log_pTM='0.222', colabfold_json_pLDDT='52.3', colabfold_json_pTM='0.42', PC1='-88.78831333582852', PC2='41.31979190633098', PC3='45.31532770748655', protein_seq='MASKQFSMLATRKSPYIKSLLLPETGPASIPDDKIRRHVKRSESTTTNLTSTTGKGMLIVYNNHPKNLVGSHYTYASDGKLRFDRNLYTAQDLSKNFNYGRKVSQLVTIKSTQLPAGVYAMQGTMNGVCIDGAPSEVETALKYETILSASTNALDKVAGVLVNDGVGVLSLPTTFDNDYIRMGDPAPSSFTPGSAQLSKPTHNPGLNSIVTAGTTGLTSGTKTISTTKTIISTDVINVDSTEGLLLDLNIQLMRWGVPSGKTATVTVDVKTVDLAGAETDAEQREIKISGTNTGRDNVITLSGLMMGLSGKKPLVAPTAAVVIEVSAISSESMTLTHSGHINNYSLTSLCAGTPGTTNPITIIIYTDLTPGGIMTVTAVSNFELIPNAELRKNIPTDFGNSDPSEMDFIKRILGQRETLELRTIWDMGMYDARRDVLSEFAHLDDNSLAMAWEWSDVLWWIKKIAGTIAPIAGAVFPAAAPLTSAISTMANAASGRALAASGKPLYRNMALAGERPLSRQITRIARTAARMTATALRSAALTPCCLRNQDACNLTADILMELTGADSCPPGISSAARLVNENNGCRCSNPSPDIKDAISAIEAGEAMDSILTAEVAQAADRPMIRTKRKARKTRTANGVELSAVGVLLPVLMDSGRRISGGAFMAVKGDLSEHIKNPKNTRIAQTVAGGTIYGLSEMVNIDEAEKLPIKGAITVLPVVQATATSILVPDNQPQLAFNSWEAAACAADTLESQQTPFLMVTGAVESGNLSPNLLAVQKQLLVAKPAGIGLAANSDRALKVVTLEQLRQVVGDKPWRKPMVTFSSGKNVAQASTNPFTSNNPFNPFMNLGDEYEEAPINPFLNLLPEAPTPPVPAPRRRPTPSPRQIAVAERFEAAAEEAAAQSPDLSDALEVANWLMETGNIQMMLDFMKRDRRGDKLSRMLFVTTYPSMAPNPGNGPTPEQARWESAVRKAGNMAATYPDITPEWVVANGYAGPDQAQAKYFSIHRRLPTAGETPIFSLGEKRKPGPDHARRLLQRLLASRDWNEEQIDALTDYVEEHGTGPDEATMQYIAQLGHNRRERPSASSRNAMKEARDAARTTAKMSLNRYKNNSGML', structure_seq='MASKQFSMLATRKSPYIKSLLLPETGPASIPDDKIRRHVKRSESTTTNLTSTTGKGMLIVYNNHPKNLVGSHYTYASDGKLRFDRNLYTAQDLSKNFNYGRKVSQLVTIKSTQLPAGVYAMQGTMNGVCIDGAPSEVETALKYETILSASTNALDKVAGVLVNDGVGVLSLPTTFDNDYIRMGDPAPSSFTPGSAQLSKPTHNPGLNSIVTAGTTGLTSGTKTISTTKTIISTDVINVDSTEGLLLDLNIQLMRWGVPSGKTATVTVDVKTVDLAGAETDAEQREIKISGTNTGRDNVITLSGLMMGLSGKKPLVAPTAAVVIEVSAISSESMTLTHSGHINNYSLTSLCAGTPGTTNPITIIIYTDLTPGGIMTVTAVSNFELIPNAELRKNIPTDFGNSDPSEMDFIKRILGQRETLELRTIWDMGMYDARRDVLSEFAHLDDNSLAMAWEWSDVLWWIKKIAGTIAPIAGAVFPAAAPLTSAISTMANAASGRALAASGKPLYRNMALAGERPLSRQITRIARTAARMTATALRSAALTPCCLRNQDACNLTADILMELTGADSCPPGISSAARLVNENNGCRCSNPSPDIKDAISAIEAGEAMDSILTAEVAQAADRPMIRTKRKARKTRTANGVELSAVGVLLPVLMDSGRRISGGAFMAVKGDLSEHIKNPKNTRIAQTVAGGTIYGLSEMVNIDEAEKLPIKGAITVLPVVQATATSILVPDNQPQLAFNSWEAAACAADTLESQQTPFLMVTGAVESGNLSPNLLAVQKQLLVAKPAGIGLAANSDRALKVVTLEQLRQVVGDKPWRKPMVTFSSGKNVAQASTNPFTSNNPFNPFMNLGDEYEEAPINPFLNLLPEAPTPPVPAPRRRPTPSPRQIAVAERFEAAAEEAAAQSPDLSDALEVANWLMETGNIQMMLDFMKRDRRGDKLSRMLFVTTYPSMAPNPGNGPTPEQARWESAVRKAGNMAATYPDITPEWVVANGYAGPDQAQAKYFSIHRRLPTAGETPIFSLGEKRKPGPDHARRLLQRLLASRDWNEEQIDALTDYVEEHGTGPDEATMQYIAQLGHNRRERPSASSRNAMKEARDAARTTAKMSLNRYKNNSGML', genome_length_bp=3579.0))])
    
    assert response.status_code == 200, f'200 was expected, but {response.status_code} was returned'
    assert protein_fetched == expected_response

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_sequence_no_match(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/proteins/sequencematch/?qualifier=NOMATCH"
    )
    assert response.status_code == 404, f'404 was expected, but {response.status_code} was returned'
    assert response.json() == {"detail": "No Matches Found"}
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_protein_structures_by_sequence_including_spaces_and_non_alphabetic_characters(mock_protein_data):
    mock_collection = AsyncMongoMockClient()["test_database"]["protein_structures"]
    await mock_collection.insert_many(mock_protein_data)

    app.dependency_overrides[get_protein_structures_collection] = lambda: mock_collection

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response1: Response = await async_client.get(
        url=f"/proteins/sequencematch/?qualifier=NO MATCH"
    )
    assert response1.status_code == 400, f'404 was expected, but {response1.status_code} was returned'
    assert response1.json() == {"detail": "Search term contains non-alphabetic characters and/or spaces. Please re-enter your sequence"}
    
    response2: Response = await async_client.get(
    url=f"/proteins/sequencematch/?qualifier=NOMATCH!"
    )
    assert response2.status_code == 400, f'404 was expected, but {response2.status_code} was returned'
    assert response2.json() == {"detail": "Search term contains non-alphabetic characters and/or spaces. Please re-enter your sequence"}
    app.dependency_overrides.clear()    