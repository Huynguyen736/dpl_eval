from abc import ABC, abstractmethod
from src.models.candidate import CandidateProfile
from src.models.job import JobDescription
from src.models.context import RetrievedContext

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, candidate: CandidateProfile, job: JobDescription, top_k_questions: int = 3) -> RetrievedContext:
        """
        Given a candidate profile and a target job description,
        retrieve the relevant interview stages, rubrics, technical questions,
        and behavioral questions to form the interview context.
        """
        pass
