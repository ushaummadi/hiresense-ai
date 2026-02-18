from pydantic import BaseModel
from typing import List, Optional, Dict

class Candidate(BaseModel):
    candidate_id: str
    filename: str
    text: str

class JobRequest(BaseModel):
    job_title: str
    job_description: str
    must_have_skills: List[str] = []
    nice_to_have_skills: List[str] = []

class RankedCandidate(BaseModel):
    candidate_id: str
    filename: str
    fit_score: float
    matched_skills: List[str]
    missing_must_haves: List[str]

class InterviewStartRequest(BaseModel):
    candidate_id: str
    job_title: str
    job_description: str

class InterviewMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class InterviewState(BaseModel):
    candidate_id: str
    messages: List[InterviewMessage]
    evaluation: Optional[Dict] = None
