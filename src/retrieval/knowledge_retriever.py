from typing import List, Dict, Any, Tuple
from src.retrieval.base import BaseRetriever
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import RetrievedContext
from src.models.framework import TechnicalQuestion, STARBehavioralQuestion, InterviewFramework
from src.preprocessing.normalizer import SkillNormalizer
from src.persistence.database import DatabaseManager

class KnowledgeGuidedRetriever(BaseRetriever):
    """
    Proposed Strategy 3:
    Knowledge-Guided Skill-Gap Hybrid Retrieval.
    Combines:
    1. Multi-signal Position Classification (Title + Family + Skills)
    2. Candidate vs. JD Skill Gap calculation
    3. Targeted Question Ranking (prioritizing missing skills & project keywords)
    4. Adaptive Level Threshold matching
    """
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()

    def classify_position(self, job: JobDescription, candidate: Optional[CandidateProfile] = None) -> str:
        import re
        t_lower = f"{job.normalized_title} {job.title} {job.job_family} {job.domain}".lower()
        skills_lower = [s.lower() for s in job.skill_requirements]
        s_text = " ".join(skills_lower)
        cand_role = (candidate.target_role + " " + candidate.category).lower() if candidate else ""

        # 0. High-specificity domain overrides (Embedded systems)
        if re.search(r"\b(embedded|firmware|vi điều khiển|microcontroller|autosar|can bus|iot|hardware)\b", t_lower) or "embedded systems" in s_text:
            return "IF_EMBEDDED"

        # 1. Candidate-aware disambiguation for polyglot / full-stack / general roles
        if candidate:
            if re.search(r"\b(automation test|tester tự động)\b", cand_role):
                return "IF_AUTO_QA"
            if re.search(r"\b(qa|qc|tester|testing)\b", cand_role) and any(w in t_lower for w in ["qa", "qc", "test", "tester"]):
                return "IF_QA_QC"
            if re.search(r"\bpython\b", cand_role) and (any("python" in s for s in skills_lower) or "python" in t_lower):
                return "IF_BE_GEN"
            if re.search(r"\bjava\b", cand_role) and (any(re.search(r"\bjava\b", s) for s in skills_lower) or "java" in t_lower):
                return "IF_BE_JAVA"
            if any(k in cand_role for k in [".net", "c#", "dotnet"]) and (any(s in [".net", "c#"] for s in skills_lower) or ".net" in t_lower or "c#" in t_lower):
                return "IF_BE_NET"
            if any(k in cand_role for k in ["react", "frontend", "web", "javascript"]) and (any(s in ["react", "vue", "angular", "javascript", "html"] for s in skills_lower) or "frontend" in t_lower or "web" in t_lower):
                return "IF_FE"
            if any(k in cand_role for k in ["data science", "machine learning", "ai"]) and any(w in t_lower for w in ["ai", "machine learning", "data"]):
                return "IF_DS" if "science" in cand_role else "IF_AI"
            if any(k in cand_role for k in ["database", "etl", "data engineer"]) and any(w in t_lower for w in ["data", "etl", "database"]):
                return "IF_DE"
            if any(k in cand_role for k in ["data analyst", "business intelligence", "bi"]) and "data" in t_lower:
                return "IF_DA"
            if any(k in cand_role for k in ["devops", "cloud"]) and any(w in t_lower for w in ["devops", "cloud", "infra"]):
                return "IF_DEVOPS"
            if any(k in cand_role for k in ["network", "sysadmin"]) and any(w in t_lower for w in ["network", "system", "infrastructure"]):
                return "IF_NETWORK"
            if any(k in cand_role for k in ["business analyst", "ba"]) and any(w in t_lower for w in ["business", "ba", "analyst"]):
                return "IF_BA"

        # 2. QA / QC
        if re.search(r"\b(automation test|automation qc|automation qa|tester tự động)\b", t_lower) or any(s in ["automation test", "selenium", "playwright", "cypress"] for s in skills_lower):
            if re.search(r"\b(qa|qc|test|tester)\b", t_lower):
                return "IF_AUTO_QA"
        if re.search(r"\b(qa|qc|tester|testing|manual test|kiểm thử)\b", t_lower):
            return "IF_QA_QC"

        # 3. Game / Unity
        if re.search(r"\b(unity|game|gameplay|unreal)\b", t_lower):
            return "IF_UNITY"

        # 4. Mobile
        if re.search(r"\b(android|kotlin)\b", t_lower):
            return "IF_MOBILE_ANDROID"
        if re.search(r"\b(ios|swift)\b", t_lower):
            return "IF_MOBILE_IOS"
        if re.search(r"\b(mobile|flutter|react native)\b", t_lower):
            return "IF_MOBILE_ANDROID"

        # 5. Embedded
        if re.search(r"\b(embedded|firmware|vi điều khiển|microcontroller|autosar|can bus|iot|hardware)\b", t_lower) or "embedded systems" in s_text:
            return "IF_EMBEDDED"

        # 6. Network & Infrastructure
        if re.search(r"\b(network|sysadmin|system engineer|hạ tầng mạng|cisco|telecom|infrastructure)\b", t_lower):
            return "IF_NETWORK"

        # 7. DevOps & Cloud
        if re.search(r"\b(devops|cloud|sre|kubernetes|ci/cd|docker)\b", t_lower):
            return "IF_DEVOPS"

        # 8. ERP
        if re.search(r"\b(erp|odoo|sap|crm)\b", t_lower):
            return "IF_ERP"

        # 9. Business Analyst & Product
        if re.search(r"\b(product engineer|growth engineer)\b", t_lower):
            return "IF_PRODUCT_ENG"
        if re.search(r"\b(business analyst|it ba|phân tích nghiệp vụ|product owner)\b", t_lower):
            return "IF_BA"

        # 10. AI & Machine Learning
        if re.search(r"\b(agentic|ai agent)\b", t_lower):
            return "IF_AGENTIC_AI"
        if re.search(r"\b(ai software|llm|rag|genai)\b", t_lower):
            return "IF_AI_SWE"
        if re.search(r"\b(ai engineer|machine learning|deep learning|nlp|computer vision|trí tuệ nhân tạo)\b", t_lower):
            return "IF_AI"

        # 11. Data (DA, DE, DS)
        if re.search(r"\b(data analyst|business intelligence|bi analyst|phân tích dữ liệu)\b", t_lower):
            return "IF_DA"
        if re.search(r"\b(data scientist|nhà khoa học dữ liệu)\b", t_lower):
            return "IF_DS"
        if re.search(r"\b(data engineer|big data|etl|data pipeline|database|dba|kho dữ liệu)\b", t_lower) or any(s in ["etl", "data warehouse", "spark", "sql server", "oracle db"] for s in skills_lower):
            return "IF_DE"

        # 12. Specific Backends
        if re.search(r"\b(java|spring boot|spring)\b", t_lower) or any(s in ["java", "spring boot", "spring"] for s in skills_lower):
            return "IF_BE_JAVA"
        if re.search(r"\b(\.net|dotnet|c#|asp\.net)\b", t_lower) or any(s in [".net", "c#", "asp.net"] for s in skills_lower):
            return "IF_BE_NET"
        if re.search(r"\b(php|laravel)\b", t_lower) or "php" in skills_lower:
            return "IF_BE_PHP"
        if re.search(r"\b(python|django|fastapi|flask|golang|go|backend|node|nodejs)\b", t_lower) or any(s in ["python", "django", "fastapi", "golang", "node.js"] for s in skills_lower):
            return "IF_BE_GEN"

        # 13. Fullstack & Frontend
        if re.search(r"\b(fullstack|full-stack|full stack)\b", t_lower):
            return "IF_FULLSTACK"
        if re.search(r"\b(frontend|front-end|react|reactjs|vue|vuejs|angular|web developer|ui/ux)\b", t_lower) or any(s in ["react", "reactjs", "vue", "angular", "html/css"] for s in skills_lower):
            return "IF_FE"

        # 15. Generic Software Engineer / Developer
        if re.search(r"\b(software engineer)\b", t_lower):
            return "IF_SWE"
        return "IF_SWD"

    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        position_id = self.classify_position(job, candidate=candidate)
        fw_dict = self.db.get_framework(position_id)
        if not fw_dict:
            fw_dict = self.db.get_framework("IF_FE")
        
        fw = InterviewFramework.model_validate(fw_dict)

        # 1. Normalize Skills
        cand_skills = set(SkillNormalizer.normalize_skill_list(candidate.technical_skills))
        job_skills = set(SkillNormalizer.normalize_skill_list(job.skill_requirements))
        
        missing_skills = job_skills - cand_skills
        matched_skills = job_skills.intersection(cand_skills)

        # 2. Candidate Context Keywords (from Projects & Experience)
        proj_texts = " ".join([f"{p.name} {p.description} {' '.join(p.tech_stack)}" for p in candidate.projects]).lower()
        exp_texts = " ".join([f"{e.company} {e.position} {' '.join(e.responsibilities)}" for e in candidate.work_experience]).lower()
        candidate_corpus = f"{proj_texts} {exp_texts}".lower()

        # 3. Score Technical Questions
        scored_questions: List[Tuple[TechnicalQuestion, float]] = []
        for q in fw.technical_questions:
            score = 1.0  # base score
            q_text = f"{q.question} {' '.join(q.key_concepts)} {q.expected_answer}".lower()

            # Boost if testing a skill missing from candidate (critical verification)
            for m_skill in missing_skills:
                if m_skill.lower() in q_text:
                    score += 3.0

            # Boost if touching an area candidate claimed project experience in (deep dive)
            for word in q.key_concepts:
                if word.lower() in candidate_corpus:
                    score += 2.0

            # Level calibration
            if candidate.current_level.lower() in q.level.lower():
                score += 1.5

            scored_questions.append((q, score))

        # Sort and take top_k
        scored_questions.sort(key=lambda x: x[1], reverse=True)
        selected_tech_qs = [q for q, _ in scored_questions[:top_k_questions]]

        # 4. Select STAR Question matching soft skills
        cand_soft = " ".join(candidate.soft_skills + candidate.behavioral_traits).lower()
        scored_star: List[Tuple[STARBehavioralQuestion, float]] = []
        for star in fw.behavioral_questions:
            score = 1.0
            if any(term in star.evaluation_focus.lower() for term in ["bug", "problem solving", "sự cố"]) and "problem solving" in cand_soft:
                score += 2.0
            if any(term in star.evaluation_focus.lower() for term in ["team", "xung đột", "giao tiếp"]) and "teamwork" in cand_soft:
                score += 2.0
            scored_star.append((star, score))
        
        scored_star.sort(key=lambda x: x[1], reverse=True)
        selected_star_qs = [s for s, _ in scored_star[:1]]

        # 5. Passing threshold
        target_level = candidate.current_level
        if target_level not in fw.passing_thresholds:
            target_level = "Fresher"
        passing_threshold = fw.passing_thresholds.get(target_level, "")

        # 6. Market Context
        companies = fw.frequently_asked_by if fw.frequently_asked_by else [c.name for c in fw.target_companies_vn]
        market_str = f"Quy trình chuẩn tại thị trường Việt Nam: {fw.vn_recruitment_process}\nCác doanh nghiệp tiêu biểu: {', '.join(companies)}"

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
            market_context=market_str,
            retrieval_strategy_used="knowledge_guided_skillgap"
        )
