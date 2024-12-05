from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class GenomeSegmentsEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True) #model_config Ensures response will always serialize with the python variable name and not the field alias name
    
    qualifier: str = Field(..., json_schema_extra={"example": "influenza A virus"})
    segments: Optional[List[GenomeCoordinatesEntry]] = None

class GenomeCoordinatesEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True) #model_config Ensures response will always serialize with the python variable name and not the field alias name
    
    nt_acc: str = Field(..., json_schema_extra={"example": "U19239.1"}, alias="_id")
    segment: str = Field(..., json_schema_extra={"example": "RNA5"})
    genome_length_bp: float = Field(..., json_schema_extra={"example": 1542})
    isolate_designation: str = Field(..., json_schema_extra={"example": "Palavas"})
    coordinates: Optional[List[GenomeCoordinates]] = None

class GenomeCoordinates(BaseModel):
    id: str = Field(..., json_schema_extra={"example": "CAX33877.1"})
    nt_acc: str = Field(..., json_schema_extra={"example": "U19239.1"})
    virus_name: str = Field(..., json_schema_extra={"example": "influenza A virus"})
    gene_name: str = Field(..., json_schema_extra={"example": "Product: neuraminidase"})
    pept_cat: str = Field(..., json_schema_extra={"example": "Protein"})
    segment: str = Field(..., json_schema_extra={"example": "RNA5"})
    start: float = Field(..., json_schema_extra={"example": 46})
    end: float = Field(..., json_schema_extra={"example": 1542})
    strand: str = Field(..., json_schema_extra={"example": "+"})
    family: str = Field(..., json_schema_extra={"example": "AAA43467.1_9914"})
    join: str = Field(..., json_schema_extra={"example": "right-join"})
