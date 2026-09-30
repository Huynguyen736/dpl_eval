import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

class Config:
    API_KEY: str = os.getenv("OPEN_API_KEY") or os.getenv("OPENAI_API_KEY") or ""
    BASE_URL: str = os.getenv("OPEN_API_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://omni.nnhlab.io.vn/v1"
    MODEL_NAME: str = os.getenv("OPEN_API_MODEL") or "agy/gemini-3.8-flash-high"
    
    # Project Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    DB_PATH: str = os.path.join(BASE_DIR, "data", "evaludate.db")
    INDEX_DIR: str = os.path.join(BASE_DIR, "data", "index")

config = Config()
