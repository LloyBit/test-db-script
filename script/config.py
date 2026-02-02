from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
    dbname: str = Field(validation_alias="POSTGRES_DB")
    admin_url: str
    database_url: str

settings = Settings()