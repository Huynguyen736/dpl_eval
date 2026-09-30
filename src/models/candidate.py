from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    gpa: Optional[Any] = None
    honors: Optional[str] = None

class WorkExperience(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    period: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)

class Project(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    tech_stack: List[str] = Field(default_factory=list)
    description: Optional[str] = None

class CandidateProfile(BaseModel):
    candidate_id: str
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    target_role: str
    category: str
    years_of_experience: float = 0.0
    current_level: str = "Fresher"
    github: Optional[str] = None
    linkedin: Optional[str] = None
    education: Optional[Education] = None
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    behavioral_traits: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    career_objective: Optional[str] = None
    source: Optional[str] = None
    raw_cv: Optional[str] = None
