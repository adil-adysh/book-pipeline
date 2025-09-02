import os
import time
import json

from typing import List, Any, Optional

from google import genai
from langchain.llms.base import LLM

from genbook.common_logger import logger

# Define default values
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL_NAME = "gemini-2.0-flash"

# --- Global Configuration Loading (Only Once) ---

# Retrieve environment variables first
temperature_env = os.getenv("GEMINI_TEMPERATURE")
model_name_env = os.getenv("GEMINI_MODEL_NAME")
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Build the path to the default config file
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "gemini_config.json")
try:
    with open(DEFAULT_CONFIG_PATH, "r") as f:
        config_data = json.load(f)
except Exception as e:
    logger.error(f"Could not load gemini config file {DEFAULT_CONFIG_PATH}: {e}")
    config_data = {}

# Determine temperature and model name with environment variables taking precedence
temperature_value = (
    temperature_env
    if temperature_env is not None
    else config_data.get("temperature", DEFAULT_TEMPERATURE)
)
try:
    temperature = float(temperature_value)
except (ValueError, TypeError) as e:
    logger.error(
        f"Could not convert temperature '{temperature_value}' to float, using default {DEFAULT_TEMPERATURE}: {e}"
    )
    temperature = DEFAULT_TEMPERATURE

model_name = model_name_env or config_data.get("model_name", DEFAULT_MODEL_NAME)

# Print the final configuration values
print(f"Using model name: {model_name}, temperature: {temperature}")


# --- Custom LLM Wrapper for Gemini API ---
class GeminiLLM(LLM):
    model_name: str = model_name
    temperature: float = temperature
    api_key: str = gemini_api_key  # Explicitly define API key
    client: genai.Client = genai.Client(api_key=api_key)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = gemini_api_key  # Ensure the API key is set
        self.model_name = model_name
        self.temperature = temperature
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

    @classmethod
    def list_models(cls) -> List[str]:
        """List available Gemini model names."""
        try:
            client = genai.Client(api_key=gemini_api_key)
            models_pager = client.models.list()
            model_names = [
                model.name.split("/", 2)[1]
                for model in models_pager
                if model.name is not None
            ]
            return model_names
        except Exception as e:
            logger.error(f"Failed to list gemini models: {e}")
            return []
