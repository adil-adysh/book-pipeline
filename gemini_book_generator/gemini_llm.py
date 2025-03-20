import os
import time
import json  # added for model config loading
import logging  # added for logging
from google import genai
from langchain.llms.base import LLM
from typing import List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve your API key from environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Default Gemini config file path (inside the package)
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "gemini_config.json")


# --- Custom LLM Wrapper for Gemini API ---
class GeminiLLM(LLM):
    api_key: str
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.7
    client: genai.Client = genai.Client(api_key=gemini_api_key)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get("api_key")
        # Load model configuration from file
        config_path = kwargs.get("config_file", DEFAULT_CONFIG_PATH)
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
            self.model_name = config_data.get("model_name", self.model_name)
            self.temperature = config_data.get("temperature", self.temperature)
            logger.info(f"Loaded config from {config_path}: {config_data}")
        except Exception as e:
            logger.warning(f"Could not load gemini config file {config_path}: {e}")
        self.client = genai.Client(api_key=self.api_key)

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _truncate_on_stop_tokens(self, text: str, stop: List[str]) -> str:
        for token in stop:
            if token in text:
                return text.split(token)[0]
        return text

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name, contents=prompt
                )
                if hasattr(response, "status_code") and response.status_code != 200:
                    raise RuntimeError(f"HTTP error: {response.status_code}")
                text = response.text.strip() if response.text else ""
                if stop:
                    text = self._truncate_on_stop_tokens(text, stop)
                return text
            except Exception as e:
                logger.error(f"Attempt {attempt} failed with error: {e}")
                if attempt == max_retries:
                    raise RuntimeError(f"Failed after {max_retries} attempts: {str(e)}")
                time.sleep(2**attempt)
        raise RuntimeError("Unexpected error in _call method")
