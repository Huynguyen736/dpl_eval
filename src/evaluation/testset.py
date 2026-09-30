from typing import List
from pydantic import BaseModel

class BenchmarkTestCase(BaseModel):
    test_id: str
    description: str
    candidate_id: str
    job_id: str
    expected_position_id: str
    expected_level: str
    expected_skills: List[str]

# Verified benchmark pairs from SQLite Database
BENCHMARK_TESTSET: List[BenchmarkTestCase] = [
    BenchmarkTestCase(
        test_id="TC_FE_01",
        description="Frontend React Fresher applied to React/Java role",
        candidate_id="CV_FE_001",
        job_id="vnw_2107318",
        expected_position_id="IF_FE",
        expected_level="Fresher",
        expected_skills=["React", "JavaScript", "HTML", "CSS"]
    ),
    BenchmarkTestCase(
        test_id="TC_JAVA_01",
        description="Java Backend Fresher applied to Java Spring Boot Engineer role",
        candidate_id="CV_JAVA_001",
        job_id="vnw_2110299",
        expected_position_id="IF_JAVA",
        expected_level="Fresher",
        expected_skills=["Java", "Spring Boot", "SQL"]
    ),
    BenchmarkTestCase(
        test_id="TC_PY_01",
        description="Python Developer applied to Python & Vue Programmer role",
        candidate_id="CV_PY_001",
        job_id="vnw_2112744",
        expected_position_id="IF_PY",
        expected_level="Fresher",
        expected_skills=["Python", "Vue.js", "SQL"]
    ),
    BenchmarkTestCase(
        test_id="TC_QA_01",
        description="QA Engineer applied to Fresher QA Engineer role",
        candidate_id="CV_QA_001",
        job_id="vnw_2106297",
        expected_position_id="IF_QA",
        expected_level="Fresher",
        expected_skills=["Manual Testing", "Automation Testing", "SQL"]
    ),
    BenchmarkTestCase(
        test_id="TC_AUTO_01",
        description="Embedded Engineer applied to Embedded Software (Flash Boot Loader) role",
        candidate_id="CV_SYS_001",
        job_id="vnw_2106484",
        expected_position_id="IF_AUTO",
        expected_level="Fresher",
        expected_skills=["C/C++", "Embedded Systems", "Microcontroller"]
    ),
    BenchmarkTestCase(
        test_id="TC_DATA_01",
        description="Data Specialist applied to Database Engineer DBA role",
        candidate_id="CV_DATA_001",
        job_id="itv_3911",
        expected_position_id="IF_DATA",
        expected_level="Fresher",
        expected_skills=["SQL", "Oracle DB", "Database"]
    )
]

def get_benchmark_testset() -> List[BenchmarkTestCase]:
    return BENCHMARK_TESTSET
