from typing import List, Dict, Any, Tuple, Optional
from src.retrieval.base import BaseRetriever
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import RetrievedContext
from src.models.framework import TechnicalQuestion, STARBehavioralQuestion, InterviewFramework
from src.preprocessing.normalizer import SkillNormalizer
from src.persistence.database import DatabaseManager
from src.persistence.store import IngestionService, BM25Index
from src.retrieval.knowledge_retriever import KnowledgeGuidedRetriever
from src.persistence.vector_store import DenseVectorIndex, ReciprocalRankFusion, SkillGapAwareReranker

class HybridRAGRetriever(BaseRetriever):
    """
    Strategy 4:
    Advanced Hybrid RAG with Knowledge Pre-Filtering, Dual-Channel Retrieval
    (Dense Latent Semantic Vectors + Sparse BM25), Reciprocal Rank Fusion (RRF),
    and Multi-Factor Skill-Gap Cross-Reranking.
    """
    def __init__(
        self,
        db: Optional[DatabaseManager] = None,
        bm25_index: Optional[BM25Index] = None,
        vector_index: Optional[DenseVectorIndex] = None,
        rrf_k: int = 60,
        w_bm25: float = 1.0,
        w_vector: float = 1.2
    ):
        self.db = db or DatabaseManager()
        ingestion = IngestionService(self.db)
        self.bm25_index = bm25_index or ingestion.get_index()
        self.vector_index = vector_index or ingestion.get_vector_index()
        self.rrf_k = rrf_k
        self.w_bm25 = w_bm25
        self.w_vector = w_vector
        self.classifier = KnowledgeGuidedRetriever(self.db)

    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        # Step 1: Pre-Filtering & Position Guard (from EDA domain separation)
        position_id = self.classifier.classify_position(job, candidate=candidate)
        fw_dict = self.db.get_framework(position_id)
        if not fw_dict:
            fw_dict = self.db.get_framework("IF_FE")
        fw = InterviewFramework.model_validate(fw_dict)

        # Step 2: Skill Gap Computation
        cand_skills = set(SkillNormalizer.normalize_skill_list(candidate.technical_skills))
        job_skills = set(SkillNormalizer.normalize_skill_list(job.skill_requirements))
        missing_skills = sorted(list(job_skills - cand_skills))
        matched_skills = sorted(list(job_skills.intersection(cand_skills)))

        # Candidate project & work corpus
        proj_texts = " ".join([f"{p.name} {p.description} {' '.join(p.tech_stack)}" for p in candidate.projects])
        exp_texts = " ".join([f"{e.company} {e.position} {' '.join(e.responsibilities)}" for e in candidate.work_experience])
        candidate_corpus = f"{proj_texts} {exp_texts}".strip()

        # Step 3: Dual-Channel Retrieval
        # Channel A: Lexical BM25 Query (Keywords, acronyms, missing skills)
        lexical_query = f"{job.normalized_title} {' '.join(missing_skills)} {' '.join(candidate.technical_skills[:8])}"
        bm25_results = self.bm25_index.search(lexical_query, top_k=100)
        # Filter BM25 to the current position_id
        bm25_pos_results = [
            (c, score) for c, score in bm25_results
            if c.get("position_id") == position_id and c.get("chunk_type") == "technical_question"
        ]
        bm25_ranked_ids = [c.get("chunk_id") for c, _ in bm25_pos_results]

        # Channel B: Dense Vector Semantic Query (Context, responsibilities, projects)
        semantic_query = f"Vị trí {fw.role_title}. Yêu cầu: {' '.join(job.must_have_requirements)}. Dự án ứng viên: {candidate_corpus}"
        dense_results = self.vector_index.search(
            semantic_query,
            top_k=100,
            position_filter=position_id
        )
        dense_pos_results = [
            (c, score) for c, score in dense_results
            if c.get("chunk_type") == "technical_question"
        ]
        dense_ranked_ids = [c.get("chunk_id") for c, _ in dense_pos_results]

        # Fallback if both lists are sparse: gather all questions in current framework
        all_fw_q_dicts = [q.model_dump() for q in fw.technical_questions]
        for q_d in all_fw_q_dicts:
            c_id = f"{fw.position_id}_{q_d.get('id')}"
            q_d["chunk_id"] = c_id
            if c_id not in bm25_ranked_ids:
                bm25_ranked_ids.append(c_id)
            if c_id not in dense_ranked_ids:
                dense_ranked_ids.append(c_id)

        # Step 4: Reciprocal Rank Fusion (RRF)
        fused_rrf = ReciprocalRankFusion.fuse(
            rankings=[(bm25_ranked_ids, self.w_bm25), (dense_ranked_ids, self.w_vector)],
            k=self.rrf_k
        )
        rrf_score_map = {doc_id: score for doc_id, score in fused_rrf}

        # Step 5: Multi-Factor Skill-Gap Cross-Reranking
        target_level = candidate.current_level or "Fresher"
        reranked = SkillGapAwareReranker.rerank(
            candidate_questions=all_fw_q_dicts,
            rrf_score_map=rrf_score_map,
            missing_skills=missing_skills,
            candidate_project_text=candidate_corpus,
            target_level=target_level
        )

        # Select top-k technical questions
        selected_tech_qs = [
            TechnicalQuestion.model_validate(q_d)
            for q_d, _ in reranked[:top_k_questions]
        ]

        # Step 6: Select Best STAR Behavioral Question
        cand_soft = " ".join(candidate.soft_skills + candidate.behavioral_traits).lower()
        scored_star: List[Tuple[STARBehavioralQuestion, float]] = []
        for star in fw.behavioral_questions:
            star_score = 1.0
            if any(term in star.evaluation_focus.lower() for term in ["bug", "problem solving", "sự cố"]) and "problem solving" in cand_soft:
                star_score += 2.5
            if any(term in star.evaluation_focus.lower() for term in ["team", "xung đột", "giao tiếp"]) and "teamwork" in cand_soft:
                star_score += 2.5
            scored_star.append((star, star_score))
        scored_star.sort(key=lambda x: x[1], reverse=True)
        selected_star_qs = [s for s, _ in scored_star[:1]]

        # Step 7: Passing Threshold & Market Context
        if target_level not in fw.passing_thresholds:
            target_level = "Fresher"
        passing_threshold = fw.passing_thresholds.get(target_level, "")

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
            retrieval_strategy_used="hybrid_rag_rrf_rerank"
        )
