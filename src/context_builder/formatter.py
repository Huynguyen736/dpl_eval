from typing import List
from src.models.context import InterviewContext

class ContextFormatter:
    """
    Formats the aggregated InterviewContext into an XML-tagged, highly structured,
    token-optimized context designed for an AI Technical Interviewer.
    """
    @staticmethod
    def format_for_llm(ctx: InterviewContext, current_stage_num: int = 2) -> str:
        cand = ctx.candidate
        job = ctx.job
        gap = ctx.skill_gap
        retrieved = ctx.retrieved_knowledge

        # Find current stage details
        cur_stage = next((s for s in retrieved.interview_stages if s.stage == current_stage_num), None)
        if not cur_stage and retrieved.interview_stages:
            cur_stage = retrieved.interview_stages[0]

        # 1. Projects summary
        projects_text = ""
        if cand.projects:
            proj_lines = []
            for p in cand.projects[:3]:
                stack = ", ".join(p.tech_stack) if p.tech_stack else "N/A"
                proj_lines.append(f"- Dự án: {p.name or 'Chưa đặt tên'} (Vai trò: {p.role or 'Thành viên'})\n  Tech stack: {stack}\n  Mô tả: {p.description or 'Không có'}")
            projects_text = "\n".join(proj_lines)
        else:
            projects_text = "- Không khai báo dự án độc lập (Tập trung vào kinh nghiệm/học thuật)."

        # 2. Work Experience summary
        exp_text = ""
        if cand.work_experience:
            exp_lines = []
            for e in cand.work_experience[:3]:
                resps = "; ".join(e.responsibilities[:2]) if e.responsibilities else "N/A"
                exp_lines.append(f"- {e.position} tại {e.company} ({e.period}): {resps}")
            exp_text = "\n".join(exp_lines)
        else:
            exp_text = "- Chưa có kinh nghiệm công tác chính thức (Fresher/Sinh viên tốt nghiệp)."

        # 3. Technical Questions with Rubrics
        tech_q_blocks = []
        for i, q in enumerate(retrieved.selected_technical_questions, 1):
            concepts = ", ".join(q.key_concepts)
            rubric_lines = "\n".join([f"    + Mức {k.upper()}: {v}" for k, v in q.scoring_rubric.items()])
            tech_q_blocks.append(
                f"  <QUESTION id=\"{q.id}\" order=\"{i}\" level=\"{q.level}\">\n"
                f"    <CONTENT>{q.question}</CONTENT>\n"
                f"    <KEY_CONCEPTS>{concepts}</KEY_CONCEPTS>\n"
                f"    <EXPECTED_ANSWER>{q.expected_answer}</EXPECTED_ANSWER>\n"
                f"    <SCORING_RUBRIC>\n{rubric_lines}\n    </SCORING_RUBRIC>\n"
                f"  </QUESTION>"
            )
        tech_questions_section = "\n".join(tech_q_blocks) if tech_q_blocks else "  (Không có câu hỏi kỹ thuật cụ thể)"

        # 4. Behavioral Questions
        star_blocks = []
        for i, s in enumerate(retrieved.selected_behavioral_questions, 1):
            star_criteria = "\n".join([f"    + {k}: {v}" for k, v in s.star_criteria.items()])
            star_blocks.append(
                f"  <STAR_QUESTION id=\"{s.id}\">\n"
                f"    <CONTENT>{s.question}</CONTENT>\n"
                f"    <EVALUATION_FOCUS>{s.evaluation_focus}</EVALUATION_FOCUS>\n"
                f"    <CRITERIA>\n{star_criteria}\n    </CRITERIA>\n"
                f"  </STAR_QUESTION>"
            )
        star_section = "\n".join(star_blocks) if star_blocks else "  (Không có câu hỏi STAR)"

        # 5. Evaluation Matrix
        matrix_lines = []
        for p in retrieved.evaluation_matrix:
            matrix_lines.append(f"  - Trụ cột '{p.pillar}' (Trọng số {p.weight_percent}%): {p.criteria}")
        matrix_section = "\n".join(matrix_lines)

        # 6. Scoring Anchors
        anchor_lines = []
        for score, desc in sorted(retrieved.scoring_anchors.items()):
            anchor_lines.append(f"  - Điểm {score}: {desc}")
        anchors_section = "\n".join(anchor_lines)

        # 7. Assembled XML Context
        formatted_prompt = f"""<MOCK_INTERVIEW_CONTEXT>

<CANDIDATE_PROFILE>
  <ID>{cand.candidate_id}</ID>
  <NAME>{cand.full_name}</NAME>
  <CURRENT_LEVEL>{cand.current_level}</CURRENT_LEVEL>
  <YEARS_OF_EXPERIENCE>{cand.years_of_experience} năm</YEARS_OF_EXPERIENCE>
  <EDUCATION>{cand.education.degree if cand.education else 'N/A'} - {cand.education.institution if cand.education else 'N/A'}</EDUCATION>
  <TECHNICAL_SKILLS>{", ".join(cand.technical_skills)}</TECHNICAL_SKILLS>
  <SOFT_SKILLS>{", ".join(cand.soft_skills + cand.behavioral_traits)}</SOFT_SKILLS>
  <PROJECTS>
{projects_text}
  </PROJECTS>
  <WORK_EXPERIENCE>
{exp_text}
  </WORK_EXPERIENCE>
</CANDIDATE_PROFILE>

<TARGET_JOB>
  <ID>{job.job_id}</ID>
  <TITLE>{job.title}</TITLE>
  <COMPANY>{job.company}</COMPANY>
  <DOMAIN>{job.domain}</DOMAIN>
  <TARGET_LEVEL>{job.levels}</TARGET_LEVEL>
  <MUST_HAVE_REQUIREMENTS>
{chr(10).join(['  - ' + req for req in job.must_have_requirements])}
  </MUST_HAVE_REQUIREMENTS>
  <PREFERRED_REQUIREMENTS>
{chr(10).join(['  - ' + req for req in job.preferred_requirements]) if job.preferred_requirements else '  - Không có yêu cầu ưu tiên đặc biệt.'}
  </PREFERRED_REQUIREMENTS>
</TARGET_JOB>

<SKILL_GAP_ANALYSIS>
  <MATCH_PERCENTAGE>{gap.match_percentage}%</MATCH_PERCENTAGE>
  <MATCHED_SKILLS>{", ".join(gap.matched_skills) if gap.matched_skills else "Chưa có kỹ năng trùng khớp trực tiếp"}</MATCHED_SKILLS>
  <MISSING_SKILLS_TO_PROBE>{", ".join(gap.missing_skills) if gap.missing_skills else "Ứng viên đáp ứng đủ các kỹ năng khai báo trong JD"}</MISSING_SKILLS_TO_PROBE>
  <EXTRA_SKILLS>{", ".join(gap.extra_skills) if gap.extra_skills else "Không có"}</EXTRA_SKILLS>
  <DIRECTIVE>Hãy chú trọng đặt câu hỏi kỹ thuật xoáy sâu vào các kỹ năng trong mục MISSING_SKILLS_TO_PROBE để xác thực ứng viên có thực sự biết hay chỉ học thuộc.</DIRECTIVE>
</SKILL_GAP_ANALYSIS>

<INTERVIEW_BLUEPRINT stage_name="{cur_stage.name if cur_stage else 'Technical Round'}" duration="{cur_stage.duration if cur_stage else '45 phút'}">
  <STAGE_FOCUS>
{chr(10).join(['  - ' + f for f in (cur_stage.focus_areas if cur_stage else [])])}
  </STAGE_FOCUS>
  <STAGE_PASSING_CRITERIA>{cur_stage.passing_criteria if cur_stage else 'N/A'}</STAGE_PASSING_CRITERIA>

  <QUESTION_POOL>
{tech_questions_section}
  </QUESTION_POOL>

  <BEHAVIORAL_QUESTION_POOL>
{star_section}
  </BEHAVIORAL_QUESTION_POOL>
</INTERVIEW_BLUEPRINT>

<EVALUATION_GUIDELINES>
  <PASSING_THRESHOLD>{retrieved.passing_threshold}</PASSING_THRESHOLD>
  <EVALUATION_MATRIX>
{matrix_section}
  </EVALUATION_MATRIX>
  <SCORING_ANCHORS_1_TO_5>
{anchors_section}
  </SCORING_ANCHORS_1_TO_5>
</EVALUATION_GUIDELINES>

</MOCK_INTERVIEW_CONTEXT>"""
        return formatted_prompt
