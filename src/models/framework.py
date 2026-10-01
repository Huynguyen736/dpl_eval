from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CompanyTarget(BaseModel):
    name: str
    program: Optional[str] = None
    career_url: Optional[str] = None

class CommunityCitation(BaseModel):
    source: str
    type: Optional[str] = None
    url: Optional[str] = None
    note: Optional[str] = None

class InterviewStage(BaseModel):
    stage_name: str
    weight_percent: Optional[int] = None
    description: Optional[str] = None
    stage: Optional[int] = None
    name: Optional[str] = None
    duration: Optional[str] = "45 phút"
    interviewer: Optional[str] = "Technical Interviewer"
    focus_areas: List[str] = Field(default_factory=list)
    passing_criteria: Optional[str] = "Đạt chuẩn kỹ thuật & tư duy giải quyết vấn đề"

    @classmethod
    def from_dict_compat(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "name" in data and "stage_name" not in data:
                data["stage_name"] = data["name"]
            if "stage_name" in data and "name" not in data:
                data["name"] = data["stage_name"]
            if not data.get("focus_areas") and data.get("description"):
                data["focus_areas"] = [data["description"]]
        return data

    def __init__(self, **data: Any):
        super().__init__(**self.from_dict_compat(data))

class EvaluationPillar(BaseModel):
    pillar: str
    pillar_en: str
    weight_percent: int
    criteria: str

class TechnicalQuestion(BaseModel):
    id: str
    question: str
    question_en: Optional[str] = None
    level: str
    key_concepts: List[str] = Field(default_factory=list)
    expected_answer: str
    scoring_rubric: Dict[str, str] = Field(default_factory=dict)
    citation_url: Optional[str] = None

class STARBehavioralQuestion(BaseModel):
    id: str
    question: str
    evaluation_focus: str
    star_criteria: Dict[str, str] = Field(default_factory=dict)

class InterviewFramework(BaseModel):
    position_id: str
    role_title: str
    major_category: str
    canonical_role_id: Optional[str] = None
    canonical_role_name: Optional[str] = None
    role_family: Optional[str] = None
    target_levels: List[str] = Field(default_factory=list)
    target_competencies: List[str] = Field(default_factory=list)
    target_companies_vn: List[CompanyTarget] = Field(default_factory=list)
    vn_recruitment_process: Optional[str] = None
    vn_community_citations: List[CommunityCitation] = Field(default_factory=list)
    frequently_asked_by: List[str] = Field(default_factory=list)
    interview_stages: List[InterviewStage] = Field(default_factory=list)
    evaluation_matrix: List[EvaluationPillar] = Field(default_factory=list)
    scoring_anchors: Dict[str, str] = Field(default_factory=dict)
    passing_thresholds: Dict[str, str] = Field(default_factory=dict)
    evaluation_rubric: Optional[Dict[str, Any]] = None
    technical_questions: List[TechnicalQuestion] = Field(default_factory=list)
    behavioral_questions: List[STARBehavioralQuestion] = Field(default_factory=list)
    questions: List[Any] = Field(default_factory=list)
    citations: List[Dict[str, str]] = Field(default_factory=list)
    markdown_file: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        # Assign stage numbers if missing
        for i, s in enumerate(self.interview_stages, 1):
            if s.stage is None:
                s.stage = i

