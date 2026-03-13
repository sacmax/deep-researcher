from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE : float = 0.1
    SEARCH_PROVIDER: str = "duckduckgo"
    MAX_SEARCH_RESULTS: int = 5
    MAX_SUB_QUESTIONS: int = 5
    PAGE_EXTRACT_CHARS: int = 2000
    DB_PATH: str = "deep_researcher.db"
    OPENAI_API_KEY: SecretStr = SecretStr("")
    TAVILY_API_KEY: SecretStr = SecretStr("")
    LANGFUSE_PUBLIC_KEY: SecretStr = SecretStr("")
    LANGFUSE_SECRET_KEY: SecretStr = SecretStr("")
    LANGFUSE_HOST: str = "https://us.cloud.langfuse.com"
    
    model_config = {"env_file": ".env"}

settings = Settings()
