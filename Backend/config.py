# backend/config.py

# TODO 1: Import BaseSettings from pydantic_settings
# TODO 2: Import lru_cache from functools
# TODO 3: Import ChatOllama from langchain_ollama

import os 
from pydantic_settings import BaseSettings
from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI

# TODO 4: Create Settings class extending BaseSettings with these fields:
#   - SNOW_INSTANCE_URL: str
#   - SNOW_USERNAME: str
#   - SNOW_PASSWORD: str
#   - OLLAMA_BASE_URL: str = "http://localhost:11434"
#   - OLLAMA_MODEL: str = "llama3.1"
#   - MEMORY_BACKEND: str = "memory"
#   - APP_ENV: str = "development"
#   - APP_HOST: str = "0.0.0.0"
#   - APP_PORT: int = 8000
#   Inside Settings add inner class Config:
#       env_file = ".env"
#       env_file_encoding = "utf-8"
class Settings(BaseSettings):
  SNOW_INSTANCE_URL: str
  SNOW_USERNAME: str
  SNOW_PASSWORD: str
  GOOGLE_API_KEY:str
  GEMINI_MODEL: str = "gemini-2.5-flash"
  MEMORY_BACKEND: str = "memory"
  APP_ENV: str = "development"
  APP_HOST: str = "0.0.0.0"
  APP_PORT: int = 8000

  class Config:
    env_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".env"
        )
    )

    env_file_encoding = "utf-8"



# TODO 5: Create get_settings() function
#   - decorate with @lru_cache()
#   - return type: Settings
#   - body: return Settings()
@lru_cache
def get_settings() ->Settings:
  return Settings() 
  

# TODO 6: Create get_llm() function
#   - return type: ChatOllama
#   - call get_settings() to get settings
#   - return ChatOllama with:
#       model=settings.OLLAMA_MODEL
#       base_url=settings.OLLAMA_BASE_URL
#       temperature=0
#       num_ctx=4096

def get_llm() -> ChatGoogleGenerativeAI:
    settings = get_settings()
    return ChatGoogleGenerativeAI(
        model=settings.GEMINI_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )