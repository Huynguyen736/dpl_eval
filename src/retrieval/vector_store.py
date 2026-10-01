"""
Backward-compatibility re-export of vector_store classes from persistence.
"""
from src.persistence.vector_store import (
    DenseVectorIndex,
    ReciprocalRankFusion,
    SkillGapAwareReranker
)

__all__ = [
    "DenseVectorIndex",
    "ReciprocalRankFusion",
    "SkillGapAwareReranker"
]
