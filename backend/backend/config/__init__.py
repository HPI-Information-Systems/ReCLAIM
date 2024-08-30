from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    SCHEMA_FILE_PATH: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings():
    return Settings()
