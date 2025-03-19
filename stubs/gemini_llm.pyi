from _typeshed import Incomplete
from google import genai
from langchain.llms.base import LLM

gemini_api_key: Incomplete

class GeminiLLM(LLM):
    api_key: str
    model_name: str
    temperature: float
    client: genai.Client
    class Config:
        arbitrary_types_allowed: bool
    def __init__(self, **kwargs) -> None: ...
