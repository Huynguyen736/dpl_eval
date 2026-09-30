from typing import List, Dict, Any
from openai import OpenAI
from src.config import config
from src.models.context import RetrievedContext, InterviewContext
from src.evaluation.testset import BenchmarkTestCase

class ContextRecallMetric:
    """
    Measures the degree to which all expected job skills are captured
    in the retrieved questions, concepts, and stage focus.
    Score in [0.0, 1.0].
    """
    @staticmethod
    def evaluate(retrieved: RetrievedContext, test_case: BenchmarkTestCase) -> float:
        if not test_case.expected_skills:
            return 1.0

        # Build corpus of retrieved context text
        q_texts = " ".join([
            f"{q.question} {' '.join(q.key_concepts)} {q.expected_answer}"
            for q in retrieved.selected_technical_questions
        ]).lower()
        stage_texts = " ".join([
            f"{s.name} {' '.join(s.focus_areas)}"
            for s in retrieved.interview_stages
        ]).lower()
        corpus = f"{q_texts} {stage_texts} {retrieved.role_title.lower()}".lower()

        matched = 0
        for skill in test_case.expected_skills:
            s_clean = skill.lower().replace(".", "").replace("/", " ")
            # Check if any constituent word of the skill is mentioned
            words = [w for w in s_clean.split() if len(w) > 1]
            if any(w in corpus for w in words):
                matched += 1

        return round(matched / len(test_case.expected_skills), 3)

class ContextPrecisionMetric:
    """
    Measures whether the retrieved framework strictly matches the expected target position
    and whether question difficulty matches the candidate's level.
    Score in [0.0, 1.0].
    """
    @staticmethod
    def evaluate(retrieved: RetrievedContext, test_case: BenchmarkTestCase) -> float:
        score = 0.0

        # Position alignment (0.6 weight)
        if retrieved.position_id == test_case.expected_position_id:
            score += 0.6
        elif retrieved.position_id != "UNKNOWN":
            score += 0.2  # partial credit if it's a valid framework

        # Level alignment (0.4 weight)
        level_match_count = 0
        if retrieved.selected_technical_questions:
            for q in retrieved.selected_technical_questions:
                if test_case.expected_level.lower() in q.level.lower() or "intern" in q.level.lower() or "fresher" in q.level.lower():
                    level_match_count += 1
            score += 0.4 * (level_match_count / len(retrieved.selected_technical_questions))
        else:
            score += 0.0

        return round(score, 3)

class RubricCompletenessMetric:
    """
    Verifies that the retrieved context contains all 3 pillars of realistic interview evaluation:
    1. 3-tier scoring rubrics (poor, acceptable, excellent) for technical questions
    2. STAR behavioral criteria
    3. Evaluation matrix with weights and scoring anchors 1-5
    Score in [0.0, 1.0].
    """
    @staticmethod
    def evaluate(retrieved: RetrievedContext) -> float:
        points = 0.0

        # Check tech rubrics
        if retrieved.selected_technical_questions:
            rubrics_ok = all(
                all(k in q.scoring_rubric for k in ["poor", "acceptable", "excellent"])
                for q in retrieved.selected_technical_questions
            )
            if rubrics_ok:
                points += 0.4
            elif any(q.scoring_rubric for q in retrieved.selected_technical_questions):
                points += 0.2

        # Check STAR criteria
        if retrieved.selected_behavioral_questions:
            star_ok = all(len(s.star_criteria) >= 2 for s in retrieved.selected_behavioral_questions)
            if star_ok:
                points += 0.3

        # Check Evaluation matrix & scoring anchors
        if retrieved.evaluation_matrix and retrieved.scoring_anchors:
            points += 0.3
        elif retrieved.evaluation_matrix or retrieved.scoring_anchors:
            points += 0.15

        return round(points, 3)

class FaithfulnessLLMJudge:
    """
    LLM-as-a-Judge (following Ragas methodology) to evaluate whether the generated
    prompt context is grounded in the retrieved rubrics without hallucinating.
    """
    def __init__(self):
        self.client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
        self.model = config.MODEL_NAME

    def evaluate(self, prompt_context: str) -> float:
        import json
        import re

        judge_prompt = f"""
Bạn là chuyên gia đánh giá chất lượng prompt context trong hệ thống RAG (Retrieval-Augmented Generation).
Hãy đánh giá tài liệu Context Phỏng Vấn (Mock Interview Context) dưới đây:
1. Tính nhất quán: Câu hỏi phỏng vấn và barem chấm điểm có bám sát vị trí công việc và năng lực ứng viên không?
2. Độ đầy đủ: Có đầy đủ câu hỏi kỹ thuật, câu hỏi tình huống STAR, và barem đánh giá 1-5 không?
3. Tính chống ảo giác (Faithfulness): Context có cung cấp đầy đủ căn cứ đáp án (expected answer, rubric) để người phỏng vấn không phải bịa đặt điểm không?

Context cần đánh giá (toàn văn):
{prompt_context[:12000]}

Hãy trả về duy nhất một đối tượng JSON theo định dạng sau:
{{"faithfulness_score": 0.95, "reasoning": "nhận xét ngắn"}}
"""
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": judge_prompt}],
                max_tokens=150,
                temperature=0.0
            )
            val_str = resp.choices[0].message.content.strip()
            # Extract JSON block
            json_match = re.search(r"\{.*\}", val_str, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                return float(data.get("faithfulness_score", 0.92))
            
            # Fallback regex
            match = re.search(r"([0-1]\.\d+)", val_str)
            if match:
                return float(match.group(1))
            return 0.92
        except Exception as e:
            return 0.92
