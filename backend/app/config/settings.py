from pydantic import BaseSettings

class Settings(BaseSettings):
    qdrant_api_key: str = ""
    qdrant_url: str = ""
    openai_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
