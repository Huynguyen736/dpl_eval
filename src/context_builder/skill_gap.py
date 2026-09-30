from typing import List, Set
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import SkillGap
from src.preprocessing.normalizer import SkillNormalizer

class SkillGapAnalyzer:
    @staticmethod
    def analyze(candidate: CandidateProfile, job: JobDescription) -> SkillGap:
        cand_norm_skills = set(SkillNormalizer.normalize_skill_list(candidate.technical_skills))
        job_norm_skills = set(SkillNormalizer.normalize_skill_list(job.skill_requirements))

        matched = sorted(list(cand_norm_skills.intersection(job_norm_skills)))
        missing = sorted(list(job_norm_skills - cand_norm_skills))
        extra = sorted(list(cand_norm_skills - job_norm_skills))

        match_pct = (len(matched) / len(job_norm_skills) * 100.0) if job_norm_skills else 100.0

        return SkillGap(
            matched_skills=matched,
            missing_skills=missing,
            extra_skills=extra,
            match_percentage=round(match_pct, 1)
        )
