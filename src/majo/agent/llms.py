from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from config import LlmConfig, LlmProvider


class LLM(BaseModel):
    config: LlmConfig

    def get_model(self) -> BaseChatModel:
        match self.config.PROVIDER:
            case LlmProvider.GOOGLE_GENAI:
                return ChatGoogleGenerativeAI(
                    model=self.config.MODEL,
                    temperature=self.config.TEMPERATURE,
                    google_api_key=self.config.API_KEY,
                )
            case _:
                raise ValueError(f"Unsupported LLM provider: {self.config.PROVIDER}")
