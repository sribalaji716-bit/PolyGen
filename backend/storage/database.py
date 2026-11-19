
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "polygen.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS generation_jobs (
                job_id TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                status TEXT NOT NULL,
                asset_path TEXT
            )
            """
        )

        columns = connection.execute(
            "PRAGMA table_info(generation_jobs)"
        ).fetchall()

        column_names = [column["name"] for column in columns]

        if "asset_path" not in column_names:
            connection.execute(
                "ALTER TABLE generation_jobs ADD COLUMN asset_path TEXT"
            )

        connection.commit()

    finally:
        connection.close()