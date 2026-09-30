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
        t_lower = f"{job.normalized_title} {job.title} {job.job_family}".lower()
        skills_lower = [s.lower() for s in job.skill_requirements]
        cand_role = (candidate.target_role + " " + candidate.category).lower() if candidate else ""

        # 1. QA / QC
        if re.search(r"\b(qa|qc|tester|testing|automation test)\b", t_lower):
            return "IF_QA"
        
        # Disambiguate polyglot / Full-Stack jobs based on candidate profile if applicable
        if candidate:
            if re.search(r"\bpython\b", cand_role) and any("python" in s for s in skills_lower):
                return "IF_PY"
            if re.search(r"\bjava\b", cand_role) and any(re.search(r"\bjava\b", s) for s in skills_lower):
                return "IF_JAVA"
            if any(k in cand_role for k in ["react", "frontend", "web", "javascript"]) and any(s in ["react", "vue", "angular", "javascript", "html"] for s in skills_lower):
                return "IF_FE"
            if any(k in cand_role for k in ["data", "etl", "database"]) and any(s in ["sql", "etl", "database", "python"] for s in skills_lower):
                return "IF_DATA"
            if any(k in cand_role for k in [".net", "c#", "dotnet"]) and any(s in [".net", "c#"] for s in skills_lower):
                return "IF_NET"

        # 2. Frontend
        if re.search(r"\b(frontend|front-end|react|reactjs|vue|angular|web developer)\b", t_lower) or any(s in ["react", "reactjs", "vue", "angular", "html/css"] for s in skills_lower):
            return "IF_FE"
        # 3. Java Backend
        if re.search(r"\b(java|spring boot|spring)\b", t_lower) or any(s in ["java", "spring boot", "spring"] for s in skills_lower):
            return "IF_JAVA"
        # 4. Python
        if re.search(r"\b(python|django|fastapi|flask)\b", t_lower) or any(s in ["python", "django", "fastapi"] for s in skills_lower):
            return "IF_PY"
        # 5. .NET
        if re.search(r"\b(\.net|dotnet|c#|asp\.net)\b", t_lower) or any(s in [".net", "c#", "asp.net"] for s in skills_lower):
            return "IF_NET"
        # 6. DevOps & Cloud
        if re.search(r"\b(devops|cloud|sre|kubernetes|ci/cd|docker)\b", t_lower):
            return "IF_DEVOPS"
        # 7. AI & Machine Learning
        if re.search(r"\b(ai engineer|machine learning|deep learning|nlp|computer vision|genai|llm)\b", t_lower):
            return "IF_AI"
        # 8. Data
        if re.search(r"\b(data engineer|data analyst|data science|etl|dba|database)\b", t_lower) or any(s in ["etl", "data warehouse", "bi", "sql"] for s in skills_lower):
            return "IF_DATA"
        # 9. Embedded / Automotive
        if re.search(r"\b(embedded|autosar|microcontroller|firmware|can bus|automotive)\b", t_lower) or any(s in ["embedded systems", "can / lin protocols", "autosar"] for s in skills_lower):
            return "IF_AUTO"
        # 10. Business Analyst
        if re.search(r"\b(business analyst|it ba)\b", t_lower):
            return "IF_BA"
        # 11. Cyber Security
        if re.search(r"\b(security|soc|pentest|cybersecurity|infosec)\b", t_lower):
            return "IF_SEC"
        # 12. UI/UX
        if re.search(r"\b(ui/ux|uiux|ux|ui designer|product designer)\b", t_lower):
            return "IF_UIUX"
        # 13. System / Network
        if re.search(r"\b(network engineer|system engineer|sysadmin|infrastructure)\b", t_lower):
            return "IF_SYS"
        # 14. Blockchain
        if re.search(r"\b(blockchain|solidity|smart contract|web3)\b", t_lower):
            return "IF_CHAIN"

        return "IF_FE"

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
        market_str = f"Quy trình chuẩn tại thị trường Việt Nam: {fw.vn_recruitment_process}\nCác doanh nghiệp tiêu biểu: {', '.join([c.name for c in fw.target_companies_vn])}"

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
