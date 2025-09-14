import os
from app.db.db_settings import DbSettings


class PostgresSettings(DbSettings):
    db_host: str = os.getenv("POSTGRES_HOST", "localhost")
    db_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    db_user: str = os.getenv("POSTGRES_USER", "agno_user")
    db_pass: str = os.getenv("POSTGRES_PASSWORD", "agno_password")
    db_database: str = os.getenv("POSTGRES_DB", "agno_db")
