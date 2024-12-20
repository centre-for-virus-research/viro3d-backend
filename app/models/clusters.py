from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class ClusterResult(BaseModel):
    genbank_id: str = Field(..., example='CAX33877.1')
    clusters: Optional[List[Cluster]] = None

class Cluster(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    cluster_representative: str = Field(..., example='CF-AFU34333.1_11502_relaxed', alias="_id")
    cluster_members: list[ClusterMember]

class ClusterMember(BaseModel):
    cluster_rep_id: str = Field(..., example='CF-AFU34333.1_11502_relaxed')
    member_record_id: str = Field(..., example="CF-CAX33877.1_11504_relaxed")
    protein_length: int = Field(..., example=1060)
    tax_id: int = Field(..., example=595652)
    species: str = Field(..., example="Ronavirus rotiferae")
    plDDT_score: float = Field(..., example=55.2),
    virus_name: str = Field(..., example="Amsacta moorei entomopoxvirus")
    family: str = Field(..., example="Poxviridae")
    host: str = Field(..., example="Choristoneura rosaceana")
    genbank_name_curated: str = Field(..., example="Gene: MSV134; Product: ORF MSV134 hypothetical protein")
    uniprot_id: str = Field(..., example="Q9YVV8"),
    genbank_id: str = Field(..., example="AFU34333.1"),
    nucleotide_accession_number: str = Field(..., example="AF063866.1")
    
    