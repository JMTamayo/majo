from enum import Enum

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings


class EmailProvider(Enum):
    """
    Represents the email provider of the email account.
    """

    GMAIL = "gmail"


class EmailConfig(BaseSettings):
    """
    Represents the configuration of the email account.
    """

    PROVIDER: EmailProvider
    EMAIL_ADDRESS: EmailStr
    PASSWORD: SecretStr


class LlmProvider(Enum):
    """
    Represents the implemented and tested LLM providers.
    """

    GOOGLE_GENAI = "google_genai"


class LlmConfig(BaseSettings):
    """
    Represents the configuration of the LLM.
    """

    PROVIDER: LlmProvider
    API_KEY: SecretStr
    MODEL: str
    TEMPERATURE: float = 0.3
