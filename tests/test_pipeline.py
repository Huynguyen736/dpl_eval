import pytest
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.preprocessing.normalizer import SkillNormalizer
from src.preprocessing.chunker import FrameworkChunker
from src.persistence.database import DatabaseManager
from src.context_builder.skill_gap import SkillGapAnalyzer
from src.context_builder.assembler import ContextAssembler
from src.retrieval.naive_retriever import NaiveRetriever
from src.retrieval.filtered_retriever import FilteredRetriever
from src.retrieval.knowledge_retriever import KnowledgeGuidedRetriever

def test_skill_normalizer():
    raw_skills = ["ReactJS", "Node.js", "C# / .NET", "Python", "unknown_tool"]
    normalized = SkillNormalizer.normalize_skill_list(raw_skills)
    assert "React" in normalized
    assert "Node.js" in normalized
    assert "C#" in normalized
    assert ".NET" in normalized
    assert "Python" in normalized

def test_database_and_candidate_loading():
    db = DatabaseManager()
    cand_dict = db.get_candidate("CV_FE_001")
    assert cand_dict is not None
    assert cand_dict["candidate_id"] == "CV_FE_001"
    assert cand_dict["category"] == "React Developer"

def test_job_loading():
    db = DatabaseManager()
    job_dict = db.get_job("vnw_2105350")
    assert job_dict is not None
    assert job_dict["job_id"] == "vnw_2105350"

def test_skill_gap_analyzer():
    cand = CandidateProfile(
        candidate_id="TEST_01",
        full_name="Tester",
        target_role="Frontend Developer",
        category="React Developer",
        technical_skills=["React", "JavaScript", "HTML", "CSS"]
    )
    job = JobDescription(
        job_id="JOB_01",
        title="Frontend React Junior",
        normalized_job_title="Frontend Developer",
        company="Tech Corp",
        job_family="Software Engineering (Frontend)",
        domain="Technology",
        levels="Junior",
        salary="15M",
        skill_requirements=["React", "TypeScript", "Redux", "HTML"],
        location="HN",
        work_mode="On-site",
        employment_type="Full-time",
        raw_job="Raw text"
    )
    gap = SkillGapAnalyzer.analyze(cand, job)
    assert "React" in gap.matched_skills
    assert "HTML" in gap.matched_skills
    assert "TypeScript" in gap.missing_skills
    assert gap.match_percentage > 0.0

def test_context_assembler_xml_structure():
    assembler = ContextAssembler()
    ctx = assembler.assemble("CV_FE_001", "vnw_2107318")
    assert ctx.raw_prompt_context is not None
    assert "<MOCK_INTERVIEW_CONTEXT>" in ctx.raw_prompt_context
    assert "<CANDIDATE_PROFILE>" in ctx.raw_prompt_context
    assert "<TARGET_JOB>" in ctx.raw_prompt_context
    assert "<SKILL_GAP_ANALYSIS>" in ctx.raw_prompt_context
    assert "<INTERVIEW_BLUEPRINT" in ctx.raw_prompt_context
    assert "<EVALUATION_GUIDELINES>" in ctx.raw_prompt_context
    assert "</MOCK_INTERVIEW_CONTEXT>" in ctx.raw_prompt_context

def test_retrieval_strategies():
    db = DatabaseManager()
    cand_dict = db.get_candidate("CV_FE_001")
    job_dict = db.get_job("vnw_2107318")
    cand = CandidateProfile.model_validate(cand_dict)
    job = JobDescription.model_validate(job_dict)

    s1 = NaiveRetriever().retrieve(cand, job)
    assert s1.retrieval_strategy_used == "naive_bm25"

    s2 = FilteredRetriever(db).retrieve(cand, job)
    assert s2.position_id == "IF_FE"

    s3 = KnowledgeGuidedRetriever(db).retrieve(cand, job)
    assert s3.position_id == "IF_FE"
    assert len(s3.selected_technical_questions) > 0
    assert len(s3.evaluation_matrix) > 0
