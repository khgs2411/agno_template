from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    """Database settings that can be set using environment variables.

    Reference: https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    # Database URL (complete connection string) - takes precedence if provided
    database_url: Optional[str] = None

    # Individual database configuration components (fallback)
    db_driver: str = "postgresql+psycopg"

    # Required for fallback if DATABASE_URL is not provided
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_user: Optional[str] = None
    db_pass: Optional[str] = None
    db_database: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_db_url(self) -> str:
        # If DATABASE_URL is provided, use it directly
        if self.database_url:
            return self.database_url

        # Otherwise, build from individual components
        db_url = "{}://{}{}@{}:{}/{}".format(
            self.db_driver,
            self.db_user,
            f":{self.db_pass}" if self.db_pass else "",
            self.db_host,
            self.db_port,
            self.db_database,
        )

        # Validate database connection
        if "None" in db_url or db_url is None:
            raise ValueError("Could not build database connection")
        return db_url
