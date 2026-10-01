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
        if re.search(r"\b(automation test|automation qc|automation qa|tester tự động)\b", t_lower):
            return "IF_AUTO_QA"
        if re.search(r"\b(qa|qc|test|tester|manual test|kiểm thử)\b", t_lower):
            return "IF_QA_QC"
        if re.search(r"\b(unity|game|gameplay|unreal)\b", t_lower):
            return "IF_UNITY"
        if re.search(r"\b(android|kotlin)\b", t_lower):
            return "IF_MOBILE_ANDROID"
        if re.search(r"\b(ios|swift)\b", t_lower):
            return "IF_MOBILE_IOS"
        if re.search(r"\b(embedded|firmware|vi điều khiển|microcontroller|autosar|can bus|iot|hardware)\b", t_lower):
            return "IF_EMBEDDED"
        if re.search(r"\b(network|sysadmin|system engineer|hạ tầng mạng|cisco|telecom|infrastructure)\b", t_lower):
            return "IF_NETWORK"
        if re.search(r"\b(devops|cloud|sre|kubernetes|ci/cd)\b", t_lower):
            return "IF_DEVOPS"
        if re.search(r"\b(erp|odoo|sap|crm)\b", t_lower):
            return "IF_ERP"
        if re.search(r"\b(product engineer|growth engineer)\b", t_lower):
            return "IF_PRODUCT_ENG"
        if re.search(r"\b(business analyst|it ba|phân tích nghiệp vụ|product owner)\b", t_lower):
            return "IF_BA"
        if re.search(r"\b(agentic|ai agent)\b", t_lower):
            return "IF_AGENTIC_AI"
        if re.search(r"\b(ai software|llm|rag|genai)\b", t_lower):
            return "IF_AI_SWE"
        if re.search(r"\b(ai engineer|machine learning|deep learning|nlp|computer vision|trí tuệ nhân tạo)\b", t_lower):
            return "IF_AI"
        if re.search(r"\b(data analyst|business intelligence|bi analyst|phân tích dữ liệu)\b", t_lower):
            return "IF_DA"
        if re.search(r"\b(data scientist|nhà khoa học dữ liệu)\b", t_lower):
            return "IF_DS"
        if re.search(r"\b(data engineer|big data|etl|data pipeline|database|dba|kho dữ liệu)\b", t_lower):
            return "IF_DE"
        # 11. Frontend
        if re.search(r"\b(frontend|front-end|react|vue|angular|web developer|ui/ux)\b", t_lower):
            return "IF_FE"

        # 12. Specific Backends
        if re.search(r"\b(java|spring)\b", t_lower):
            return "IF_BE_JAVA"
        if re.search(r"\b(\.net|dotnet|c#|asp\.net)\b", t_lower):
            return "IF_BE_NET"
        if re.search(r"\b(php|laravel)\b", t_lower):
            return "IF_BE_PHP"
        if re.search(r"\b(python|django|fastapi|golang|go|backend|node|nodejs)\b", t_lower):
            return "IF_BE_GEN"

        # 13. Fullstack
        if re.search(r"\b(fullstack|full-stack|full stack)\b", t_lower):
            return "IF_FULLSTACK"
        if re.search(r"\b(software engineer)\b", t_lower):
            return "IF_SWE"
        return "IF_FE"

    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        position_id = self._map_title_to_position(f"{job.normalized_title} {job.title} {job.job_family}", job.domain)
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
