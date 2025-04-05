import logging
import os
from functools import lru_cache
from pydantic_settings import BaseSettings

from logger import logger

class Settings(BaseSettings):

    environment: str = os.getenv("environment", "dev")
    testing: bool = os.getenv("testing", False)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "GEMINI_API_KEY")


@lru_cache()
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()