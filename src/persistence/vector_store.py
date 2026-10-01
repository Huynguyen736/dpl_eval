import os
import re
import math
import pickle
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import svds

class DenseVectorIndex:
    """
    Dense Semantic Vector Space Index.
    Projects text chunks into a continuous dense latent semantic space using
    subword/word n-gram TF-IDF and SVD (Latent Semantic Analysis).
    Computes exact Cosine Similarity for semantic query matching.
    """
    def __init__(self, dim: int = 64):
        self.dim = dim
        self.doc_ids: List[str] = []
        self.chunks: List[Dict[str, Any]] = []
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.doc_vectors: Optional[np.ndarray] = None
        self.components: Optional[np.ndarray] = None

    def _tokenize(self, text: str) -> List[str]:
        words = re.findall(r'[\w#\+\.]+', text.lower())
        tokens = list(words)
        for i in range(len(words) - 1):
            tokens.append(f"{words[i]}_{words[i+1]}")
        return tokens

    def build_index(self, chunks: List[Dict[str, Any]]):
        self.chunks = chunks
        self.doc_ids = [c.get("chunk_id", str(i)) for i, c in enumerate(chunks)]
        if not chunks:
            return

        doc_tokens = [self._tokenize(c.get("searchable_text", "")) for c in chunks]
        N = len(chunks)
        df: Dict[str, int] = {}
        for tokens in doc_tokens:
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1

        self.vocab = {term: idx for idx, (term, count) in enumerate(df.items()) if count >= 1}
        self.idf = {term: math.log((N + 1) / (df[term] + 1)) + 1.0 for term in self.vocab}

        rows, cols, data = [], [], []
        for i, tokens in enumerate(doc_tokens):
            tf: Dict[str, int] = {}
            for t in tokens:
                if t in self.vocab:
                    tf[t] = tf.get(t, 0) + 1
            for t, count in tf.items():
                rows.append(i)
                cols.append(self.vocab[t])
                data.append(count * self.idf[t])

        X = sp.csr_matrix((data, (rows, cols)), shape=(N, max(1, len(self.vocab))))
        k = min(self.dim, N - 1, len(self.vocab) - 1)
        if k >= 3:
            u, s, vt = svds(X, k=k)
            vecs = u * s
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.doc_vectors = vecs / norms
            self.components = vt
        else:
            arr = X.toarray()
            norms = np.linalg.norm(arr, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.doc_vectors = arr / norms
            self.components = None

    def search(self, query: str, top_k: int = 10, position_filter: Optional[str] = None) -> List[Tuple[Dict[str, Any], float]]:
        if self.doc_vectors is None or not self.chunks:
            return []

        tokens = self._tokenize(query)
        tf: Dict[str, int] = {}
        for t in tokens:
            if t in self.vocab:
                tf[t] = tf.get(t, 0) + 1

        q_vec = np.zeros(len(self.vocab))
        for t, count in tf.items():
            q_vec[self.vocab[t]] = count * self.idf[t]

        if self.components is not None:
            dense_q = q_vec @ self.components.T
        else:
            dense_q = q_vec

        norm = np.linalg.norm(dense_q)
        if norm > 0:
            dense_q = dense_q / norm

        sims = self.doc_vectors @ dense_q
        indices = np.argsort(-sims)

        results: List[Tuple[Dict[str, Any], float]] = []
        for idx in indices:
            c = self.chunks[idx]
            if position_filter and c.get("position_id") != position_filter:
                continue
            score = float(sims[idx])
            results.append((c, score))
            if len(results) >= top_k:
                break

        return results

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump((self.doc_ids, self.chunks, self.vocab, self.idf, self.doc_vectors, self.components), f)

    def load(self, filepath: str):
        with open(filepath, "rb") as f:
            self.doc_ids, self.chunks, self.vocab, self.idf, self.doc_vectors, self.components = pickle.load(f)


class ReciprocalRankFusion:
    """
    Reciprocal Rank Fusion (RRF) algorithm to merge multiple retrieval rankings
    (e.g., Sparse Lexical BM25 and Dense Vector Cosine Similarity) without requiring
    score scale calibration.
    Formula: RRF_score(d) = sum( weight_i / (k + rank_i(d)) )
    """
    @staticmethod
    def fuse(
        rankings: List[Tuple[List[str], float]],
        k: int = 60
    ) -> List[Tuple[str, float]]:
        combined_scores: Dict[str, float] = {}

        for doc_ids, weight in rankings:
            for rank, doc_id in enumerate(doc_ids, 1):
                rrf_val = weight / (k + rank)
                combined_scores[doc_id] = combined_scores.get(doc_id, 0.0) + rrf_val

        sorted_items = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_items


class SkillGapAwareReranker:
    """
    Multi-Factor Cross-Reranker that re-scores candidate questions from RRF
    by combining:
    1. Base RRF Rank Score
    2. Missing Skills Probe Priority (+2.5 per covered missing skill)
    3. Project Proof Deep Dive (+2.0 for concepts mentioned in candidate projects)
    4. Level Calibration (+1.5 for matching target level)
    5. Rubric Completeness Guard (+0.5 for complete 3-tier rubrics)
    """
    @staticmethod
    def rerank(
        candidate_questions: List[Dict[str, Any]],
        rrf_score_map: Dict[str, float],
        missing_skills: List[str],
        candidate_project_text: str,
        target_level: str
    ) -> List[Tuple[Dict[str, Any], float]]:
        scored: List[Tuple[Dict[str, Any], float]] = []
        c_proj_lower = candidate_project_text.lower()
        missing_lower = [m.lower() for m in missing_skills]

        for q_dict in candidate_questions:
            c_id = q_dict.get("chunk_id", "")
            q_id = q_dict.get("id", "")
            # Check both full chunk_id (e.g. IF_FE_FE_Q01) and short id (FE_Q01)
            base_score = max(
                rrf_score_map.get(c_id, 0.0),
                rrf_score_map.get(q_id, 0.0)
            ) * 100.0

            q_text = (q_dict.get("question", "") + " " +
                      " ".join(q_dict.get("key_concepts", [])) + " " +
                      q_dict.get("expected_answer", "")).lower()

            # 1. Missing skill verification boost (probe missing JD skills)
            gap_boost = 0.0
            for m_skill in missing_lower:
                if m_skill in q_text:
                    gap_boost += 3.0

            # 2. Project proof boost (testing claims from candidate projects / experience)
            proj_boost = 0.0
            if c_proj_lower:
                for term in re.findall(r'[a-zA-Z]{3,}', q_text):
                    if term in c_proj_lower and term not in ["trong", "cho", "khi", "nhu", "voi", "duoc", "khong"]:
                        proj_boost += 0.5
                        if proj_boost >= 2.5:
                            break

            # 3. Level alignment boost (strict matching)
            level_boost = 0.0
            q_level = str(q_dict.get("level", "")).lower()
            t_level = target_level.lower()
            if t_level == q_level:
                level_boost = 2.0
            elif ("fresher" in t_level and "intern" in q_level) or ("junior" in t_level and "fresher" in q_level):
                level_boost = 1.0

            # 4. Rubric completeness boost
            rubric = q_dict.get("scoring_rubric", {})
            rubric_boost = 0.5 if all(k in rubric for k in ["poor", "acceptable", "excellent"]) else 0.0

            total_score = base_score + gap_boost + proj_boost + level_boost + rubric_boost
            scored.append((q_dict, total_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
