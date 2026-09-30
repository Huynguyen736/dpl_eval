import re
from typing import List, Set, Dict

# Canonical mapping of common IT skill variations & compound labels
CANONICAL_SKILL_MAP: Dict[str, List[str]] = {
    # Frontend
    "react": ["React"],
    "reactjs": ["React"],
    "react.js": ["React"],
    "react native": ["React Native"],
    "vue": ["Vue.js"],
    "vuejs": ["Vue.js"],
    "angular": ["Angular"],
    "angularjs": ["Angular"],
    "typescript": ["TypeScript"],
    "ts": ["TypeScript"],
    "javascript": ["JavaScript"],
    "js": ["JavaScript"],
    "html": ["HTML"],
    "html5": ["HTML"],
    "css": ["CSS"],
    "css3": ["CSS"],
    "sass": ["Sass"],
    "tailwind": ["Tailwind CSS"],
    "tailwind css": ["Tailwind CSS"],
    "nextjs": ["Next.js"],
    "next.js": ["Next.js"],
    "redux": ["Redux"],
    
    # Backend & Languages
    "node": ["Node.js"],
    "nodejs": ["Node.js"],
    "node.js": ["Node.js"],
    "express": ["Express.js"],
    "expressjs": ["Express.js"],
    "python": ["Python"],
    "django": ["Django"],
    "fastapi": ["FastAPI"],
    "flask": ["Flask"],
    "java": ["Java"],
    "spring": ["Spring Boot"],
    "spring boot": ["Spring Boot"],
    "c#": ["C#"],
    "c# / .net": ["C#", ".NET"],
    ".net": [".NET"],
    "dotnet": [".NET"],
    "asp.net": ["ASP.NET"],
    "c/c++": ["C", "C++"],
    "c++": ["C++"],
    "c": ["C"],
    "golang": ["Go"],
    "go": ["Go"],
    "php": ["PHP"],
    
    # Database
    "sql": ["SQL"],
    "mysql": ["MySQL"],
    "postgresql": ["PostgreSQL"],
    "postgres": ["PostgreSQL"],
    "mongodb": ["MongoDB"],
    "redis": ["Redis"],
    "oracle": ["Oracle DB"],
    "sql server": ["SQL Server"],
    "sqlite": ["SQLite"],
    
    # Cloud & DevOps & Infra
    "docker": ["Docker"],
    "kubernetes": ["Kubernetes"],
    "k8s": ["Kubernetes"],
    "aws": ["AWS"],
    "azure": ["Azure"],
    "gcp": ["GCP"],
    "ci/cd": ["CI/CD"],
    "cicd": ["CI/CD"],
    "jenkins": ["Jenkins"],
    "linux": ["Linux"],
    "git": ["Git"],
    "git / gitflow": ["Git"],
    "gitflow": ["Git"],
    
    # AI & Data
    "machine learning": ["Machine Learning"],
    "ml": ["Machine Learning"],
    "ai/ml": ["Machine Learning", "AI"],
    "deep learning": ["Deep Learning"],
    "nlp": ["NLP"],
    "computer vision": ["Computer Vision"],
    "pytorch": ["PyTorch"],
    "tensorflow": ["TensorFlow"],
    "pandas": ["Pandas"],
    "numpy": ["NumPy"],
    "llm / genai": ["LLM", "Generative AI"],
    "llm": ["LLM"],
    "etl": ["ETL"],
    
    # Methodology & Testing
    "agile": ["Agile"],
    "scrum": ["Scrum"],
    "agile / scrum": ["Agile", "Scrum"],
    "jira": ["JIRA"],
    "selenium": ["Selenium"],
    "automation test": ["Automation Testing"],
    "manual test": ["Manual Testing"],
    "unit test": ["Unit Testing"],
    "restful api": ["REST API"],
    "rest api": ["REST API"],
    "rest/grpc": ["REST API", "gRPC"],
    "graphql": ["GraphQL"],
    "embedded systems": ["Embedded Systems"],
    "can / lin protocols": ["CAN/LIN Protocols"],
    "autosar": ["AUTOSAR"]
}

class SkillNormalizer:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Lowercase, trim extra whitespaces
        text = text.strip()
        text = re.sub(r"\s+", " ", text)
        return text

    @classmethod
    def normalize_single_skill(cls, skill: str) -> List[str]:
        cleaned = cls.clean_text(skill).lower()
        if not cleaned:
            return []
        
        # Exact lookup in canonical map
        if cleaned in CANONICAL_SKILL_MAP:
            return CANONICAL_SKILL_MAP[cleaned]
        
        # Split compounds with slash or ampersand if applicable
        if " / " in cleaned:
            subparts = cleaned.split(" / ")
            res = []
            for part in subparts:
                res.extend(cls.normalize_single_skill(part))
            if res:
                return list(set(res))

        # Fallback: title-case the cleaned skill
        return [skill.strip()]

    @classmethod
    def normalize_skill_list(cls, skills: List[str]) -> List[str]:
        result_set: Set[str] = set()
        for skill in skills:
            if not skill:
                continue
            normalized_items = cls.normalize_single_skill(skill)
            for item in normalized_items:
                if item:
                    result_set.add(item)
        return sorted(list(result_set))
