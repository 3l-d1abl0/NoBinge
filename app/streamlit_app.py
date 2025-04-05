from config import get_settings, Settings
from logger import logger


settings: Settings = get_settings()

if __name__ == "__main__":
    logger.info('############NoBinge#############')
    logger.info(settings)