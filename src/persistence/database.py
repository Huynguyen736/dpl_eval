import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from src.config import config

class DatabaseManager:
    def __init__(self, db_path: str = config.DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Candidates table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                candidate_id TEXT PRIMARY KEY,
                full_name TEXT,
                target_role TEXT,
                category TEXT,
                current_level TEXT,
                years_of_experience REAL,
                normalized_skills TEXT,
                data_json TEXT
            );
            """)

            # 2. Jobs table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT,
                normalized_title TEXT,
                job_family TEXT,
                domain TEXT,
                levels TEXT,
                company TEXT,
                normalized_skills TEXT,
                data_json TEXT
            );
            """)

            # 3. Frameworks table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS frameworks (
                position_id TEXT PRIMARY KEY,
                role_title TEXT,
                major_category TEXT,
                data_json TEXT
            );
            """)

            # 4. Knowledge Chunks table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_chunks (
                chunk_id TEXT PRIMARY KEY,
                chunk_type TEXT,
                position_id TEXT,
                role_title TEXT,
                searchable_text TEXT,
                metadata_json TEXT
            );
            """)

            # Indices for rapid filtering
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_role ON candidates(target_role);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_candidates_level ON candidates(current_level);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_norm_title ON jobs(normalized_title);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_level ON jobs(levels);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_position ON knowledge_chunks(position_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_type ON knowledge_chunks(chunk_type);")

            conn.commit()

    def insert_candidate(self, candidate_id: str, full_name: str, target_role: str,
                         category: str, current_level: str, yoe: float,
                         normalized_skills: List[str], data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO candidates 
            (candidate_id, full_name, target_role, category, current_level, years_of_experience, normalized_skills, data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (candidate_id, full_name, target_role, category, current_level, yoe,
                  json.dumps(normalized_skills, ensure_ascii=False),
                  json.dumps(data, ensure_ascii=False)))

    def insert_job(self, job_id: str, title: str, normalized_title: str,
                   job_family: str, domain: str, levels: str, company: str,
                   normalized_skills: List[str], data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO jobs 
            (job_id, title, normalized_title, job_family, domain, levels, company, normalized_skills, data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (job_id, title, normalized_title, job_family, domain, levels, company,
                  json.dumps(normalized_skills, ensure_ascii=False),
                  json.dumps(data, ensure_ascii=False)))

    def insert_framework(self, position_id: str, role_title: str, major_category: str, data: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO frameworks (position_id, role_title, major_category, data_json)
            VALUES (?, ?, ?, ?)
            """, (position_id, role_title, major_category, json.dumps(data, ensure_ascii=False)))

    def insert_chunk(self, chunk_id: str, chunk_type: str, position_id: str,
                     role_title: str, searchable_text: str, metadata: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO knowledge_chunks 
            (chunk_id, chunk_type, position_id, role_title, searchable_text, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (chunk_id, chunk_type, position_id, role_title, searchable_text,
                  json.dumps(metadata, ensure_ascii=False)))

    def get_candidate(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT data_json FROM candidates WHERE candidate_id = ?", (candidate_id,)).fetchone()
            return json.loads(row["data_json"]) if row else None

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT data_json FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            return json.loads(row["data_json"]) if row else None

    def get_framework(self, position_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT data_json FROM frameworks WHERE position_id = ?", (position_id,)).fetchone()
            return json.loads(row["data_json"]) if row else None

    def get_chunks_by_position(self, position_id: str, chunk_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            if chunk_type:
                cursor = conn.execute("SELECT * FROM knowledge_chunks WHERE position_id = ? AND chunk_type = ?", (position_id, chunk_type))
            else:
                cursor = conn.execute("SELECT * FROM knowledge_chunks WHERE position_id = ?", (position_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM knowledge_chunks").fetchall()
            return [dict(r) for r in rows]
