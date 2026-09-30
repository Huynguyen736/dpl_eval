from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExperienceRequirement(BaseModel):
    min_years: Optional[float] = None
    max_years: Optional[float] = None
    raw_text: Optional[str] = None
    confidence: Optional[float] = None

class JobDescription(BaseModel):
    job_id: str
    title: str = Field(alias="tên job")
    normalized_title: str = Field(alias="normalized_job_title")
    company: str
    job_family: str
    domain: str
    levels: str
    salary: str = Field(alias="mức lương")
    skill_requirements: List[str] = Field(default_factory=list)
    experience: Optional[ExperienceRequirement] = None
    education_requirements: Optional[str] = None
    language_requirements: Optional[str] = None
    must_have_requirements: List[str] = Field(default_factory=list)
    preferred_requirements: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    behavioral_traits: List[str] = Field(default_factory=list)
    certification_requirements: Optional[str] = None
    portfolio_requirements: Optional[str] = None
    benefits: List[str] = Field(default_factory=list)
    location: str
    work_mode: str
    employment_type: str
    raw_job: str = Field(alias="raw job")

    model_config = {"populate_by_name": True}
