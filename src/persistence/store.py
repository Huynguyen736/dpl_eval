import os
import json
import pickle
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi

from src.config import config
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.framework import InterviewFramework
from src.preprocessing.normalizer import SkillNormalizer
from src.preprocessing.chunker import FrameworkChunker, KnowledgeChunk
from src.persistence.database import DatabaseManager
from src.persistence.vector_store import DenseVectorIndex

class BM25Index:
    def __init__(self):
        self.doc_ids: List[str] = []
        self.corpus_chunks: List[Dict[str, Any]] = []
        self.bm25: BM25Okapi = None

    def build_index(self, chunks: List[Dict[str, Any]]):
        self.corpus_chunks = chunks
        self.doc_ids = [c["chunk_id"] for c in chunks]
        tokenized_corpus = [c["searchable_text"].lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not self.bm25 or not self.corpus_chunks:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = []
        for idx in top_indices:
            if scores[idx] > 0.0:
                results.append((self.corpus_chunks[idx], float(scores[idx])))
        return results

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump((self.doc_ids, self.corpus_chunks, self.bm25), f)

    def load(self, filepath: str):
        with open(filepath, "rb") as f:
            self.doc_ids, self.corpus_chunks, self.bm25 = pickle.load(f)

class IngestionService:
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
        self.bm25_index = BM25Index()
        self.vector_index = DenseVectorIndex(dim=64)
        self.index_path = os.path.join(config.INDEX_DIR, "bm25_chunks.pkl")
        self.vector_index_path = os.path.join(config.INDEX_DIR, "dense_vector_chunks.pkl")

    def run_full_ingestion(self) -> Dict[str, int]:
        print("[IngestionService] Starting full ingestion pipeline...")
        
        # 1. Ingest Frameworks & Chunks
        frameworks_path = os.path.join(config.DATA_DIR, "interview_frameworks.json")
        with open(frameworks_path, "r", encoding="utf-8") as f:
            raw_frameworks = json.load(f)
        
        all_chunks: List[Dict[str, Any]] = []
        for fw_dict in raw_frameworks:
            fw = InterviewFramework.model_validate(fw_dict)
            self.db.insert_framework(
                position_id=fw.position_id,
                role_title=fw.role_title,
                major_category=fw.major_category,
                data=fw.model_dump()
            )
            # Create semantic chunks
            chunks = FrameworkChunker.chunk_framework(fw)
            for chunk in chunks:
                chunk_dict = chunk.model_dump()
                self.db.insert_chunk(
                    chunk_id=chunk.chunk_id,
                    chunk_type=chunk.chunk_type.value,
                    position_id=chunk.position_id,
                    role_title=chunk.role_title,
                    searchable_text=chunk.searchable_text,
                    metadata=chunk.metadata
                )
                all_chunks.append({
                    "chunk_id": chunk.chunk_id,
                    "chunk_type": chunk.chunk_type.value,
                    "position_id": chunk.position_id,
                    "role_title": chunk.role_title,
                    "searchable_text": chunk.searchable_text,
                    "metadata": chunk.metadata
                })

        # Build & save BM25 index on all chunks
        self.bm25_index.build_index(all_chunks)
        self.bm25_index.save(self.index_path)

        # Build & save Dense Vector index on all chunks
        self.vector_index.build_index(all_chunks)
        self.vector_index.save(self.vector_index_path)

        print(f"[IngestionService] Ingested {len(raw_frameworks)} frameworks into {len(all_chunks)} semantic chunks (BM25 + Dense Vectors).")

        # 2. Ingest Candidates
        candidates_path = os.path.join(config.DATA_DIR, "candidates.json")
        with open(candidates_path, "r", encoding="utf-8") as f:
            raw_candidates = json.load(f)

        for c_dict in raw_candidates:
            c = CandidateProfile.model_validate(c_dict)
            norm_skills = SkillNormalizer.normalize_skill_list(c.technical_skills)
            self.db.insert_candidate(
                candidate_id=c.candidate_id,
                full_name=c.full_name,
                target_role=c.target_role,
                category=c.category,
                current_level=c.current_level,
                yoe=c.years_of_experience,
                normalized_skills=norm_skills,
                data=c.model_dump()
            )
        print(f"[IngestionService] Ingested {len(raw_candidates)} candidates.")

        # 3. Ingest Jobs
        jobs_path = os.path.join(config.DATA_DIR, "jobs_below_mid.json")
        with open(jobs_path, "r", encoding="utf-8") as f:
            raw_jobs = json.load(f)

        for j_dict in raw_jobs:
            j = JobDescription.model_validate(j_dict)
            norm_skills = SkillNormalizer.normalize_skill_list(j.skill_requirements)
            self.db.insert_job(
                job_id=j.job_id,
                title=j.title,
                normalized_title=j.normalized_title,
                job_family=j.job_family,
                domain=j.domain,
                levels=j.levels,
                company=j.company,
                normalized_skills=norm_skills,
                data=j.model_dump(by_alias=True)
            )
        print(f"[IngestionService] Ingested {len(raw_jobs)} jobs.")

        return {
            "frameworks": len(raw_frameworks),
            "chunks": len(all_chunks),
            "candidates": len(raw_candidates),
            "jobs": len(raw_jobs)
        }

    def get_index(self) -> BM25Index:
        if not self.bm25_index.bm25:
            if os.path.exists(self.index_path):
                self.bm25_index.load(self.index_path)
            else:
                chunks = self.db.get_all_chunks()
                self.bm25_index.build_index(chunks)
                self.bm25_index.save(self.index_path)
        return self.bm25_index

    def get_vector_index(self) -> DenseVectorIndex:
        if self.vector_index.doc_vectors is None:
            if os.path.exists(self.vector_index_path):
                self.vector_index.load(self.vector_index_path)
            else:
                chunks = self.db.get_all_chunks()
                self.vector_index.build_index(chunks)
                self.vector_index.save(self.vector_index_path)
        return self.vector_index
