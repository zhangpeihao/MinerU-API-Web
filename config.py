from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    API_BASE_URL: str = "https://mineru.net/api/v4"
    API_TOKEN: str
    MAX_FILES: int = 200
    MAX_FILE_SIZE_MB: int = 200
    MAX_PAGES: int = 600

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()