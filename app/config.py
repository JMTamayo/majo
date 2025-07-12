from enum import Enum

from pydantic import SecretStr, EmailStr
from pydantic_settings import BaseSettings


class EmailProvider(Enum):
    OUTLOOK = "outlook"


class EmailConfig(BaseSettings):
    PROVIDER: EmailProvider
    EMAIL_ADDRESS: EmailStr
    PASSWORD: SecretStr


class LlmProvider(Enum):
    GOOGLE_GENAI = "google_genai"
    OPENAI = "openai"


class LlmConfig(BaseSettings):
    PROVIDER: LlmProvider
    API_KEY: SecretStr
    MODEL: str
    TEMPERATURE: float = 0.3
