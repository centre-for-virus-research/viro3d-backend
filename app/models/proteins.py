from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class ProteinStructure(BaseModel):

    model_config = ConfigDict(populate_by_name=True) #model_config Ensures response will always serialize with the python variable name and not the field alias name
    
    record_id: str = Field(..., json_schema_extra={"example": "CAX33877.1_11504"}, alias="_id") 
    uniprot_id: str = Field(..., json_schema_extra={"example": "P03648"})
    pept_cat: str = Field(..., json_schema_extra={"example": "protein"})
    protlen: int = Field(..., json_schema_extra={"example": 1060})
    genbank_name_curated: str = Field(..., json_schema_extra={"example": "Product: neuraminidase"})
    gene: Optional[str] = Field(..., json_schema_extra={"example": "NPH I"})
    product: Optional[str] = Field(..., json_schema_extra={"example": "polyprotein"})
    note: Optional[str] = Field(..., json_schema_extra={"example": "G6L"})
    genbank_id: str = Field(..., json_schema_extra={"example": "AAB39411.1"}, alias="protein_id")
    mat_pept_id: Optional[str] = Field(..., json_schema_extra={"example": "CAX33877.1.4"})
    reg_id: Optional[str] = Field(..., json_schema_extra={"example": "AGZ63355.1.1.1"})
    uniq_id: str = Field(..., json_schema_extra={"example": "AGZ63355.1.1.1"})
    uniprot_match_status: str = Field(..., json_schema_extra={"example": "no_match"})
    nt_acc: str = Field(..., json_schema_extra={"example": "U19239.1"})
    acc: str = Field(..., json_schema_extra={"example": "U19239"})
    seg: Optional[str] = Field(..., json_schema_extra={"example": "SegA"})
    taxid: int = Field(..., json_schema_extra={"example": 595652})
    Sort: int = Field(..., json_schema_extra={"example": 11505})
    Realm: Optional[str] = Field(..., json_schema_extra={"example": "Riboviria"})
    Subrealm: Optional[str] = ...
    Kingdom: Optional[str] = Field(..., json_schema_extra={"example": "Orthornavirae"})
    Subkingdom: Optional[str] = ...
    Phylum: Optional[str] = Field(..., json_schema_extra={"example": "Nucleocytoviricota"})
    Subphylum: Optional[str] = Field(..., json_schema_extra={"example": "Polyploviricotina"}) 
    Class: Optional[str] = Field(..., json_schema_extra={"example": "Pokkesviricetes"})
    Subclass: Optional[str] = Field(..., json_schema_extra={"example": ""})
    Order: Optional[str] = Field(..., json_schema_extra={"example": "Chitovirales"})
    Suborder: Optional[str] = Field(..., json_schema_extra={"example": "Arnidovirineae"}) 
    Family: str = Field(..., json_schema_extra={"example": "Poxviridae"})
    Subfamily: str = Field(..., json_schema_extra={"example": "Entomopoxvirinae"})
    Genus: Optional[str] = Field(..., json_schema_extra={"example": "Ronavirus"})
    Subgenus: Optional[str] = Field(..., json_schema_extra={"example": "Acimevirus"}) 
    Species: str = Field(..., json_schema_extra={"example": "Choristoneura fumiferana entomopoxvirus"})
    Exemplar_or_additional_isolate: str = Field(..., alias="Exemplar or additional isolate")
    Virus_name_s_: Optional[str] = Field(..., alias="Virus name(s)")
    Virus_name_abbreviation_s_: Optional[str] = Field(..., alias="Virus name abbreviation(s)")
    Virus_isolate_designation: Optional[str] = Field(..., alias="Virus isolate designation")
    Virus_REFSEQ_accession: Optional[str] = Field(..., alias="Virus REFSEQ accession")
    Genome_coverage: str = Field(..., alias="Genome coverage")
    Genome_composition: str = Field(..., alias="Genome composition")
    Host_source: str = Field(..., alias="Host source")
    host: Optional[str] = Field(...)
    genbank_genome_coordinates: str
    genome_coordinates: str
    protein_coordinates: str
    esmfold_log_pLDDT: Optional[str] = Field(...)
    esmfold_log_pTM: Optional[str] = Field(...)
    colabfold_json_pLDDT: str
    colabfold_json_pTM: str
    PC1: str = Field(..., json_schema_extra={"example": "-217.7728352516993"})
    PC2: str = Field(..., json_schema_extra={"example": "-307.89330874240665"})
    PC3: str = Field(..., json_schema_extra={"example": "-181.53899797364755"})
    protein_seq: str = Field(..., json_schema_extra={"example": "GALQAAPKATAQKQIQAPTPRARQPQRPQAEQTPLQKLLMRTMEEES"})
    structure_seq: str = Field(..., json_schema_extra={"example": "GALQAAPKATAQKQIQAPTPRARQPQRPQAEQTPLQKLLMRTMEEES"})
    genome_length_bp: float = Field(..., json_schema_extra={"example": 800.0})

class RecordIDEntry(BaseModel):
    record_id: str = Field(..., json_schema_extra={"example": "AHV82114.1.1.6_10921"})
    protein_structure: ProteinStructure = None
    
class ProteinNameEntry(BaseModel):
    proteinname: str = Field(..., json_schema_extra={"example": "Product: polymerase 1"})
    count: int = Field(..., json_schema_extra={"example": 100})
    protein_structures: Optional[List[ProteinStructure]] = None

class GenbankEntry(BaseModel):
    genbank_id: str = Field(..., json_schema_extra={"example": "CAX33877.1"})
    count: int = Field(..., json_schema_extra={"example": 100})
    protein_structures: Optional[List[ProteinStructure]] = None

class VirusEntry(BaseModel):
    virus_name: str = Field(..., json_schema_extra={"example": "influenza A virus"})
    count: int = Field(..., json_schema_extra={"example": 100})
    protein_structures: Optional[List[ProteinStructure]] = None

class BlastMatch(BaseModel):
    structure_id: str = Field(..., json_schema_extra={"example": "CAX33877.1.6_11504"})
    score: float = Field(..., json_schema_extra={"example": 48.0})
    evalue: float = Field(..., json_schema_extra={"example": 1.25458})
    hit_length: int = Field(..., json_schema_extra={"example": 11})
    positives: int = Field(..., json_schema_extra={"example": 11})
    gaps: int = Field(..., json_schema_extra={"example": 3})
    protein_structure: ProteinStructure = Field(...)

class BlastEntry(BaseModel):
    sequence: str = Field(..., json_schema_extra={"example": "MRMRLLA"})
    matches: List[BlastMatch] = None