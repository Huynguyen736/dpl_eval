from typing import List
from src.retrieval.base import BaseRetriever
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import RetrievedContext
from src.models.framework import TechnicalQuestion, STARBehavioralQuestion, InterviewStage, EvaluationPillar
from src.persistence.store import BM25Index, IngestionService

class NaiveRetriever(BaseRetriever):
    """
    Baseline Strategy 1:
    Pure lexical BM25 search across all raw knowledge chunks without metadata filtering.
    """
    def __init__(self, index: BM25Index = None):
        self.index = index or IngestionService().get_index()

    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        # Formulate a flat keyword query from candidate skills and job title
        skills_str = " ".join(candidate.technical_skills[:10])
        query = f"{job.title} {job.normalized_title} {skills_str}"
        
        # Search all chunks globally
        raw_results = self.index.search(query, top_k=top_k_questions * 3)

        selected_tech_qs: List[TechnicalQuestion] = []
        selected_star_qs: List[STARBehavioralQuestion] = []
        selected_stages: List[InterviewStage] = []
        eval_matrix: List[EvaluationPillar] = []

        position_id = "UNKNOWN"
        role_title = job.normalized_title

        for chunk, score in raw_results:
            c_type = chunk.get("chunk_type")
            meta = chunk.get("metadata", {})
            position_id = chunk.get("position_id", position_id)
            role_title = chunk.get("role_title", role_title)

            if c_type == "technical_question" and len(selected_tech_qs) < top_k_questions:
                try:
                    selected_tech_qs.append(TechnicalQuestion.model_validate(meta))
                except Exception:
                    pass
            elif c_type == "star_question" and len(selected_star_qs) < 1:
                try:
                    selected_star_qs.append(STARBehavioralQuestion.model_validate(meta))
                except Exception:
                    pass
            elif c_type == "stage_guide" and len(selected_stages) < 2:
                try:
                    selected_stages.append(InterviewStage.model_validate(meta))
                except Exception:
                    pass
            elif c_type == "evaluation_rubric" and not eval_matrix:
                try:
                    eval_matrix = [EvaluationPillar.model_validate(p) for p in meta.get("evaluation_matrix", [])]
                except Exception:
                    pass

        return RetrievedContext(
            position_id=position_id,
            role_title=role_title,
            target_level=candidate.current_level,
            interview_stages=selected_stages,
            evaluation_matrix=eval_matrix,
            scoring_anchors={},
            passing_threshold="",
            selected_technical_questions=selected_tech_qs,
            selected_behavioral_questions=selected_star_qs,
            market_context=None,
            retrieval_strategy_used="naive_bm25"
        )
