import os
import yaml
from functools import lru_cache
from pydantic_settings import BaseSettings
import threading


from logger import logger

class Settings(BaseSettings):

    environment: str = os.getenv("environment", "dev")
    testing: bool = os.getenv("testing", False)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "GEMINI_API_KEY")

    # Model Configuration
    embed_model: str =  os.getenv("embed_model")
    # Interval between frames in seconds
    frame_interval: int = os.getenv("frame_interval")

    # Source
    indexing_path: str =  os.getenv("indexing_path")
    data_dir: str =  os.getenv("data_dir")
    video_dir: str =  os.getenv("video_dir")

    # Retrieval Configuration
    similarity_top_k: int =  os.getenv("similarity_top_k")
    image_similarity_top_k: int =  os.getenv("image_similarity_top_k")


    # Video Processing Configuration
    # Maximum number of frames to extract
    max_frames: int =  os.getenv("max_frames")
    # Minimum segment length in seconds
    min_segment_length: int =  os.getenv("min_segment_length")
    # Maximum segment length in seconds
    max_segment_length: int =  os.getenv("max_segment_length")

    # UI Configuration
    # Maximum number of frames to display in UI
    max_display_frames: int =  os.getenv("max_display_frames")
    frame_display_columns: int =  os.getenv("frame_display_columns")


@lru_cache()
def get_envs() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()
