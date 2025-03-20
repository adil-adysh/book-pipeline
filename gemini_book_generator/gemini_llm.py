import os
import time
import json

from typing import List, Any, Optional

from google import genai
from langchain.llms.base import LLM

from gemini_book_generator.common_logger import logger

# Define default values
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL_NAME = "gemini-2.0-flash"

# --- Retrieve Configuration for Temperature and Model Name ---

# Attempt to read environment variables first
temperature_env = os.getenv("GEMINI_TEMPERATURE")
model_name_env = os.getenv("GEMINI_MODEL_NAME")

# Build the path to the config file and load it if available
config_path = os.path.join(os.path.dirname(__file__), "gemini_config.json")
try:
    with open(config_path, "r") as f:
        config_data = json.load(f)
    logger.info(f"Loaded config from {config_path}: {config_data}")
except Exception as e:
    logger.warning(f"Could not load gemini config file {config_path}: {e}")
    config_data = {}

# For temperature, environment variable takes precedence over config file,
# and we fallback to a default if neither is provided.
temperature_value = (
    temperature_env
    if temperature_env is not None
    else config_data.get("temperature", DEFAULT_TEMPERATURE)
)
try:
    temperature = float(temperature_value)
except (ValueError, TypeError) as e:
    logger.warning(
        f"Could not convert temperature '{temperature_value}' to float, using default {DEFAULT_TEMPERATURE}: {e}"
    )
    temperature = DEFAULT_TEMPERATURE

# For model name, use environment variable if available, otherwise fallback to config/default.
model_name = model_name_env or config_data.get("model_name", DEFAULT_MODEL_NAME)

# Retrieve your API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Use the loaded config file path as the default config path for the package.
DEFAULT_CONFIG_PATH = config_path


# --- Custom LLM Wrapper for Gemini API ---
class GeminiLLM(LLM):
    api_key: str
    model_name: str = model_name
    temperature: float = temperature
    client: genai.Client = genai.Client(api_key=gemini_api_key)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get("api_key", gemini_api_key)
        # Load model configuration from file, if provided
        config_path_local = kwargs.get("config_file", DEFAULT_CONFIG_PATH)
        try:
            with open(config_path_local, "r") as f:
                config_data_local = json.load(f)
            self.model_name = config_data_local.get("model_name", self.model_name)
            temp_val = config_data_local.get("temperature", self.temperature)
            try:
                self.temperature = float(temp_val)
            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Could not convert temperature '{temp_val}' to float, using default {self.temperature}: {e}"
                )
            logger.info(f"Loaded config from {config_path_local}: {config_data_local}")
        except Exception as e:
            logger.warning(
                f"Could not load gemini config file {config_path_local}: {e}"
            )
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
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            models_pager = client.models.list()
            model_names = [
                model.name for model in models_pager if model.name is not None
            ]
            logger.info("Available Gemini models: %s", model_names)
            return model_names
        except Exception as e:
            logger.error("Failed to list gemini models: %s", e)
            return []
