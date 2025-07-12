from langchain_core.language_models import BaseLLM
from pydantic import BaseModel

from config import LlmConfig
from agent.llms import LLM


class Majo(BaseModel):
    llm: BaseLLM

    def __init__(self, llm_config: LlmConfig):
        super().__init__(
            llm=LLM(config=llm_config).get_model(),
        )

    def _get_llm(self) -> BaseLLM:
        return self.llm

    def invoke(self, query: str) -> str:
        return self.llm.invoke(query)
