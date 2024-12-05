from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field

class VirusName(BaseModel):
    search_term: str = Field(..., json_schema_extra={"example": "influenza A virus"})
    count: int = Field(..., json_schema_extra={"example": 100})
    viruses: List[dict]