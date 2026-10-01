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
from src.retrieval.hybrid_rag_retriever import HybridRAGRetriever
from src.persistence.vector_store import DenseVectorIndex, ReciprocalRankFusion, SkillGapAwareReranker

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

def test_framework_all_25_loaded_and_validated():
    import json
    import os
    from src.config import config
    from src.models.framework import InterviewFramework

    fw_path = os.path.join(config.DATA_DIR, "interview_frameworks.json")
    with open(fw_path, "r", encoding="utf-8") as f:
        raw_list = json.load(f)

    assert len(raw_list) == 25, f"Expected 25 frameworks, got {len(raw_list)}"

    db = DatabaseManager()
    for item in raw_list:
        fw = InterviewFramework.model_validate(item)
        assert fw.position_id is not None
        assert fw.role_title is not None
        assert len(fw.interview_stages) >= 3
        assert len(fw.technical_questions) >= 5
        assert len(fw.behavioral_questions) >= 2
        assert len(fw.evaluation_matrix) >= 3

        # Verify DB persistence
        db_fw = db.get_framework(fw.position_id)
        assert db_fw is not None
        assert db_fw["position_id"] == fw.position_id

def test_multirole_knowledge_retrieval():
    from src.evaluation.testset import get_benchmark_testset

    db = DatabaseManager()
    kg = KnowledgeGuidedRetriever(db)
    testset = get_benchmark_testset()

    for tc in testset:
        c_dict = db.get_candidate(tc.candidate_id)
        j_dict = db.get_job(tc.job_id)
        c = CandidateProfile.model_validate(c_dict)
        j = JobDescription.model_validate(j_dict)
        ret = kg.retrieve(c, j)
        assert ret.position_id == tc.expected_position_id, f"Failed for {tc.test_id}: expected {tc.expected_position_id}, got {ret.position_id}"

def test_framework_chunker_new_stages():
    from src.models.framework import InterviewFramework

    db = DatabaseManager()
    fw_dict = db.get_framework("IF_FE")
    fw = InterviewFramework.model_validate(fw_dict)
    chunks = FrameworkChunker.chunk_framework(fw)

    stage_chunks = [c for c in chunks if c.chunk_type.value == "stage_guide"]
    assert len(stage_chunks) == len(fw.interview_stages)
    for sc in stage_chunks:
        assert "Stage" in sc.searchable_text
        assert sc.metadata.get("stage_name") is not None

def test_hybrid_rag_strategy_4():
    db = DatabaseManager()
    cand_dict = db.get_candidate("CV_FE_001")
    job_dict = db.get_job("vnw_2107318")
    cand = CandidateProfile.model_validate(cand_dict)
    job = JobDescription.model_validate(job_dict)

    s4 = HybridRAGRetriever(db=db)
    ctx = s4.retrieve(cand, job, top_k_questions=3)

    assert ctx.retrieval_strategy_used == "hybrid_rag_rrf_rerank"
    assert ctx.position_id == "IF_FE"
    assert len(ctx.selected_technical_questions) == 3
    assert len(ctx.selected_behavioral_questions) == 1
    assert len(ctx.evaluation_matrix) > 0
    assert ctx.passing_threshold != ""
    assert ctx.market_context is not None

    # Test RRF fusion directly
    rankings = [
        (["doc_A", "doc_B", "doc_C"], 1.0),
        (["doc_B", "doc_C", "doc_D"], 1.2)
    ]
    fused = ReciprocalRankFusion.fuse(rankings, k=60)
    assert len(fused) == 4
    # doc_B should rank highest because it appears at rank 2 in list1 and rank 1 in list2
    top_doc, _ = fused[0]
    assert top_doc == "doc_B"


