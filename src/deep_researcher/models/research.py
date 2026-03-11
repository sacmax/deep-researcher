from pydantic import Field, BaseModel
from datetime import datetime
from typing import Literal

class Source(BaseModel):
    url: str
    title: str
    snippet: str

class Claim(BaseModel):
    text: str
    source_url: str
    confidence: float = Field(ge=0.0, le=1.0)
    sub_question_id: str

class SubQuestion(BaseModel):
    id: str
    question: str
    rationale: str
    priority: int = Field(ge=1, le=10)

class BranchResult(BaseModel):
    sub_question_id: str
    claims: list[Claim]
    search_queries_used: list[str]
    sources: list[Source]

class Contradiction(BaseModel):
    claim_a: Claim
    claim_b: Claim
    explanation: str
    severity: Literal["low", "medium", "high"]

class ResearchReport(BaseModel):
    question: str
    answer: str
    claims: list[Claim]
    contradictions: list[Contradiction]
    knowledge_gaps: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    sources: list[Source]
    generated_at: datetime