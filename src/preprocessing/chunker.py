from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from src.models.framework import InterviewFramework

class ChunkType(str, Enum):
    TECHNICAL_QUESTION = "technical_question"
    STAR_QUESTION = "star_question"
    STAGE_GUIDE = "stage_guide"
    EVALUATION_RUBRIC = "evaluation_rubric"

class KnowledgeChunk(BaseModel):
    chunk_id: str
    chunk_type: ChunkType
    position_id: str
    role_title: str
    target_levels: List[str] = Field(default_factory=list)
    searchable_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class FrameworkChunker:
    @staticmethod
    def chunk_framework(framework: InterviewFramework) -> List[KnowledgeChunk]:
        chunks: List[KnowledgeChunk] = []

        # 1. Chunk Technical Questions
        for q in framework.technical_questions:
            # Construct a rich searchable text
            concepts = ", ".join(q.key_concepts)
            searchable_text = f"Role: {framework.role_title} | Level: {q.level}\nQuestion: {q.question}\nKey Concepts: {concepts}\nExpected Answer: {q.expected_answer}"
            chunks.append(
                KnowledgeChunk(
                    chunk_id=f"{framework.position_id}_{q.id}",
                    chunk_type=ChunkType.TECHNICAL_QUESTION,
                    position_id=framework.position_id,
                    role_title=framework.role_title,
                    target_levels=framework.target_levels,
                    searchable_text=searchable_text,
                    metadata=q.model_dump()
                )
            )

        # 2. Chunk STAR Behavioral Questions
        for star in framework.behavioral_questions:
            searchable_text = f"Role: {framework.role_title} | STAR Behavioral\nQuestion: {star.question}\nFocus: {star.evaluation_focus}"
            chunks.append(
                KnowledgeChunk(
                    chunk_id=f"{framework.position_id}_{star.id}",
                    chunk_type=ChunkType.STAR_QUESTION,
                    position_id=framework.position_id,
                    role_title=framework.role_title,
                    target_levels=framework.target_levels,
                    searchable_text=searchable_text,
                    metadata=star.model_dump()
                )
            )

        # 3. Chunk Interview Stages
        for stage in framework.interview_stages:
            focus = "; ".join(stage.focus_areas)
            searchable_text = f"Role: {framework.role_title} | Stage {stage.stage}: {stage.name} ({stage.duration})\nInterviewer: {stage.interviewer}\nFocus: {focus}\nPassing Criteria: {stage.passing_criteria}"
            chunks.append(
                KnowledgeChunk(
                    chunk_id=f"{framework.position_id}_STAGE_{stage.stage}",
                    chunk_type=ChunkType.STAGE_GUIDE,
                    position_id=framework.position_id,
                    role_title=framework.role_title,
                    target_levels=framework.target_levels,
                    searchable_text=searchable_text,
                    metadata=stage.model_dump()
                )
            )

        # 4. Chunk Evaluation Rubric & Matrix
        matrix_text = "\n".join([f"- {p.pillar} ({p.weight_percent}%): {p.criteria}" for p in framework.evaluation_matrix])
        anchors_text = "\n".join([f"Score {k}: {v}" for k, v in framework.scoring_anchors.items()])
        thresholds_text = "\n".join([f"Level {k}: {v}" for k, v in framework.passing_thresholds.items()])
        searchable_rubric = f"Role: {framework.role_title} Evaluation Matrix:\n{matrix_text}\nScoring Anchors:\n{anchors_text}\nThresholds:\n{thresholds_text}"
        
        chunks.append(
            KnowledgeChunk(
                chunk_id=f"{framework.position_id}_RUBRIC",
                chunk_type=ChunkType.EVALUATION_RUBRIC,
                position_id=framework.position_id,
                role_title=framework.role_title,
                target_levels=framework.target_levels,
                searchable_text=searchable_rubric,
                metadata={
                    "evaluation_matrix": [p.model_dump() for p in framework.evaluation_matrix],
                    "scoring_anchors": framework.scoring_anchors,
                    "passing_thresholds": framework.passing_thresholds
                }
            )
        )

        return chunks
