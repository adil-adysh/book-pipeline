import logging

logger = logging.getLogger("gemini_app")
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
