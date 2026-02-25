from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ProfileType(str, Enum):
    BUYER = "BUYER"
    TARGET = "TARGET"
    PROSPECT = "PROSPECT"


class Confidence(str, Enum):
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class FieldWithEvidence(BaseModel):
    value: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.MED


class NumericField(BaseModel):
    value: Optional[float] = None
    evidence: List[str] = Field(default_factory=list)


class RevenueField(NumericField):
    period: Optional[str] = None


class EBITDAField(NumericField):
    label: Optional[str] = None


class MarketCapField(NumericField):
    as_of: Optional[date] = None


class CompanyInput(BaseModel):
    name: str


class BusinessOverview(BaseModel):
    overall: FieldWithEvidence = Field(default_factory=FieldWithEvidence)
    segments: FieldWithEvidence = Field(default_factory=FieldWithEvidence)
    clients: FieldWithEvidence = Field(default_factory=FieldWithEvidence)
    industrial_setup: FieldWithEvidence = Field(default_factory=FieldWithEvidence)


class Financials(BaseModel):
    revenue: RevenueField = Field(default_factory=RevenueField)
    ebitda: EBITDAField = Field(default_factory=EBITDAField)
    market_cap: MarketCapField = Field(default_factory=MarketCapField)
    employees: NumericField = Field(default_factory=NumericField)


class OwnershipEntry(BaseModel):
    name: str
    stake: Optional[float] = None
    type: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)
    round: Optional[str] = None


class Ownership(BaseModel):
    rule_applied: int = 4
    entries: List[OwnershipEntry] = Field(default_factory=list)
    note: Optional[str] = None


class Region(BaseModel):
    region: str
    evidence: List[str] = Field(default_factory=list)


class Geography(BaseModel):
    hq: FieldWithEvidence = Field(default_factory=FieldWithEvidence)
    operating_regions: List[Region] = Field(default_factory=list)
    map_image_path: Optional[str] = None


class Transaction(BaseModel):
    year: int
    type: str
    counterparty: str
    value: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)


class Person(BaseModel):
    name: str
    role: str
    evidence: List[str] = Field(default_factory=list)


class People(BaseModel):
    executives: List[Person] = Field(default_factory=list)
    board: List[Person] = Field(default_factory=list)


class Narrative(BaseModel):
    value: Optional[str] = None
    evidence: List[str] = Field(default_factory=list)
    internal_only: bool = False


class Narratives(BaseModel):
    buyer_rationale: Narrative = Field(default_factory=Narrative)
    prospect_talking_points: Narrative = Field(default_factory=lambda: Narrative(internal_only=True))


class Quality(BaseModel):
    missing_fields: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)


class EvidenceObject(BaseModel):
    source_id: str
    title: str
    url: str
    publisher: str
    doc_type: str
    locator: str
    accessed_at: datetime
    snippet: str


class Profile(BaseModel):
    profile_id: UUID = Field(default_factory=uuid4)
    profile_type: ProfileType
    company_input: CompanyInput
    business_overview: BusinessOverview = Field(default_factory=BusinessOverview)
    financials: Financials = Field(default_factory=Financials)
    ownership: Ownership = Field(default_factory=Ownership)
    geography: Geography = Field(default_factory=Geography)
    transactions: List[Transaction] = Field(default_factory=list)
    people: People = Field(default_factory=People)
    narratives: Narratives = Field(default_factory=Narratives)
    quality: Quality = Field(default_factory=Quality)
    evidence: Dict[str, EvidenceObject] = Field(default_factory=dict)
    exported_pptx_path: Optional[str] = None


class ProfileCreateRequest(BaseModel):
    profile_type: ProfileType
    company_name: str


class ProfilePatchRequest(BaseModel):
    fields: Dict[str, str]
