from typing import List, Optional
from src.retrieval.base import BaseRetriever
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import RetrievedContext
from src.models.framework import TechnicalQuestion, STARBehavioralQuestion, InterviewStage, EvaluationPillar, InterviewFramework
from src.persistence.database import DatabaseManager

class FilteredRetriever(BaseRetriever):
    """
    Baseline Strategy 2:
    Matches job title to position_id, then retrieves chunks exclusively from that framework.
    """
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def _map_title_to_position(self, title: str, domain: str) -> str:
        import re
        t_lower = (title + " " + domain).lower()
        if re.search(r"\b(qa|qc|test|tester|automation)\b", t_lower):
            return "IF_QA"
        if re.search(r"\b(frontend|react|vue|angular|web)\b", t_lower):
            return "IF_FE"
        if re.search(r"\b(java|spring)\b", t_lower):
            return "IF_JAVA"
        if re.search(r"\b(python|django|fastapi)\b", t_lower):
            return "IF_PY"
        if re.search(r"\b(\.net|c#|dotnet|asp\.net)\b", t_lower):
            return "IF_NET"
        if re.search(r"\b(devops|cloud|sre)\b", t_lower):
            return "IF_DEVOPS"
        if re.search(r"\b(machine learning|deep learning|nlp|computer vision|ai engineer)\b", t_lower):
            return "IF_AI"
        if re.search(r"\b(data|etl|dba|bi|database)\b", t_lower):
            return "IF_DATA"
        if re.search(r"\b(security|soc|pentest)\b", t_lower):
            return "IF_SEC"
        if re.search(r"\b(embedded|automotive|autosar|firmware)\b", t_lower):
            return "IF_AUTO"
        if re.search(r"\b(business analyst|it ba)\b", t_lower):
            return "IF_BA"
        if re.search(r"\b(robot|slam|ros)\b", t_lower):
            return "IF_ROBOT"
        if re.search(r"\b(ui/ux|ui designer|product designer)\b", t_lower):
            return "IF_UIUX"
        if re.search(r"\b(blockchain|solidity|web3)\b", t_lower):
            return "IF_CHAIN"
        if re.search(r"\b(system|network|infrastructure)\b", t_lower):
            return "IF_SYS"
        return "IF_FE"

    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        position_id = self._map_title_to_position(job.normalized_title, job.domain)
        fw_dict = self.db.get_framework(position_id)
        if not fw_dict:
            # Fallback to first available
            fw_dict = self.db.get_framework("IF_FE")
        
        fw = InterviewFramework.model_validate(fw_dict)

        # Select top technical questions
        selected_tech_qs = fw.technical_questions[:top_k_questions]
        selected_star_qs = fw.behavioral_questions[:1]

        target_level = candidate.current_level if candidate.current_level in fw.passing_thresholds else "Fresher"
        passing_threshold = fw.passing_thresholds.get(target_level, "")

        return RetrievedContext(
            position_id=fw.position_id,
            role_title=fw.role_title,
            target_level=target_level,
            interview_stages=fw.interview_stages,
            evaluation_matrix=fw.evaluation_matrix,
            scoring_anchors=fw.scoring_anchors,
            passing_threshold=passing_threshold,
            selected_technical_questions=selected_tech_qs,
            selected_behavioral_questions=selected_star_qs,
            market_context=fw.vn_recruitment_process,
            retrieval_strategy_used="filtered_metadata"
        )
