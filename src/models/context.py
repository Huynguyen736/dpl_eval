from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.framework import TechnicalQuestion, STARBehavioralQuestion, InterviewStage, EvaluationPillar

class SkillGap(BaseModel):
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    extra_skills: List[str] = Field(default_factory=list)
    match_percentage: float = 0.0

class RetrievedContext(BaseModel):
    position_id: str
    role_title: str
    target_level: str
    interview_stages: List[InterviewStage] = Field(default_factory=list)
    evaluation_matrix: List[EvaluationPillar] = Field(default_factory=list)
    scoring_anchors: Dict[str, str] = Field(default_factory=dict)
    passing_threshold: str = ""
    selected_technical_questions: List[TechnicalQuestion] = Field(default_factory=list)
    selected_behavioral_questions: List[STARBehavioralQuestion] = Field(default_factory=list)
    market_context: Optional[str] = None
    retrieval_strategy_used: str = "knowledge_guided"

class InterviewContext(BaseModel):
    candidate: CandidateProfile
    job: JobDescription
    skill_gap: SkillGap
    retrieved_knowledge: RetrievedContext
    raw_prompt_context: Optional[str] = None
