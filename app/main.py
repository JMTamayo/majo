from pydantic import SecretStr
from typer import Typer, Option, Argument
from rich import print as rprint

from config import LlmConfig, EmailProvider, EmailConfig, LlmProvider
from agent.agent import Majo

app = Typer(pretty_exceptions_show_locals=False)


@app.command()
def agent(
    query: str = Argument(
        ...,
        help="The query to interact with the agent. E.g.: 'Have I received emails from the company's CEO?'",
    ),
    llm_provider: LlmProvider = Option(
        ...,
        help="The large language model provider",
        envvar="LLM_PROVIDER",
        prompt=True,
    ),
    llm_api_key: str = Option(
        ...,
        help="the API key to authenticate with the llm provider",
        envvar="LLM_API_KEY",
        prompt=True,
    ),
    llm_model: str = Option(
        ..., help="The model to use for the llm", envvar="LLM_MODEL", prompt=True
    ),
    email_provider: EmailProvider = Option(
        ...,
        help="The email service provider",
        envvar="EMAIL_PROVIDER",
        prompt=True,
    ),
    email_address: str = Option(
        ...,
        help="The email address. E.g.: 'john.doe@example.com'",
        envvar="EMAIL_ADDRESS",
        prompt=True,
    ),
    email_password: str = Option(
        ...,
        help="The email password.",
        envvar="EMAIL_PASSWORD",
        prompt=True,
    ),
):
    llm_config = LlmConfig(
        PROVIDER=llm_provider,
        API_KEY=SecretStr(llm_api_key),
        MODEL=llm_model,
    )

    email_config = EmailConfig(
        PROVIDER=email_provider,
        EMAIL_ADDRESS=email_address,
        PASSWORD=SecretStr(email_password),
    )

    agent = Majo(llm_config=llm_config)
    rprint(agent.invoke(query))

if __name__ == "__main__":
    app()