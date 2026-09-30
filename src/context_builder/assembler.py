from typing import Optional, Union, Dict, Any
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import InterviewContext, RetrievedContext
from src.context_builder.skill_gap import SkillGapAnalyzer
from src.context_builder.formatter import ContextFormatter
from src.retrieval.base import BaseRetriever
from src.retrieval.knowledge_retriever import KnowledgeGuidedRetriever
from src.persistence.database import DatabaseManager

class ContextAssembler:
    """
    High-level orchestrator that coordinates:
    Candidate + Job -> Retriever -> SkillGapAnalyzer -> ContextFormatter -> Final LLM Context.
    """
    def __init__(self, retriever: Optional[BaseRetriever] = None, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self.retriever = retriever or KnowledgeGuidedRetriever(self.db)

    def assemble(self, candidate: Union[str, CandidateProfile, Dict[str, Any]],
                 job: Union[str, JobDescription, Dict[str, Any]],
                 stage_num: int = 2) -> InterviewContext:
        # Resolve candidate
        if isinstance(candidate, str):
            c_dict = self.db.get_candidate(candidate)
            if not c_dict:
                raise ValueError(f"Candidate ID {candidate} not found in database.")
            candidate_obj = CandidateProfile.model_validate(c_dict)
        elif isinstance(candidate, dict):
            candidate_obj = CandidateProfile.model_validate(candidate)
        else:
            candidate_obj = candidate

        # Resolve job
        if isinstance(job, str):
            j_dict = self.db.get_job(job)
            if not j_dict:
                raise ValueError(f"Job ID {job} not found in database.")
            job_obj = JobDescription.model_validate(j_dict)
        elif isinstance(job, dict):
            job_obj = JobDescription.model_validate(job)
        else:
            job_obj = job

        # 1. Retrieve knowledge
        retrieved_knowledge = self.retriever.retrieve(candidate_obj, job_obj)

        # 2. Analyze skill gap
        skill_gap = SkillGapAnalyzer.analyze(candidate_obj, job_obj)

        # 3. Create context container
        ctx = InterviewContext(
            candidate=candidate_obj,
            job=job_obj,
            skill_gap=skill_gap,
            retrieved_knowledge=retrieved_knowledge
        )

        # 4. Format into token-efficient XML prompt context
        ctx.raw_prompt_context = ContextFormatter.format_for_llm(ctx, current_stage_num=stage_num)

        return ctx
