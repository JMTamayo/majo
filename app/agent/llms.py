from langchain_core.language_models import BaseLLM
from langchain_google_genai import GoogleGenerativeAI
from pydantic import BaseModel

from config import LlmConfig, LlmProvider


class LLM(BaseModel):
    config: LlmConfig

    def get_model(self) -> BaseLLM:
        match self.config.PROVIDER:
            case LlmProvider.GOOGLE_GENAI:
                return GoogleGenerativeAI(
                    google_api_key=self.config.API_KEY.get_secret_value(),
                    model=self.config.MODEL,
                    temperature=self.config.TEMPERATURE,
                )
            case _:
                raise ValueError(f"Unsupported LLM provider: {self.config.PROVIDER}")
