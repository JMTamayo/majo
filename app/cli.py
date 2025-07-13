from pydantic import SecretStr
from typer import Typer, Option, Context

from config import LlmConfig, EmailProvider, EmailConfig, LlmProvider
from agent.agent import Majo

app = Typer(pretty_exceptions_show_locals=False)


@app.callback()
def main(
    ctx: Context,
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
    llm_config: LlmConfig = LlmConfig(
        PROVIDER=llm_provider,
        API_KEY=SecretStr(llm_api_key),
        MODEL=llm_model,
    )
    email_config: EmailConfig = EmailConfig(
        PROVIDER=email_provider,
        EMAIL_ADDRESS=email_address,
        PASSWORD=SecretStr(email_password),
    )

    agent: Majo = Majo(llm_config=llm_config)

    ctx.meta["AGENT"] = agent


@app.command()
def inbox_report(
    ctx: Context,
    max_emails: int = Option(
        50,
        help="The maximum number of emails to report.",
        prompt=False,
    ),
):
    """
    Generate a report of the emails in your inbox that you haven't yet read, organizing them by priority level.
    """
    agent: Majo = ctx.meta["AGENT"]
    agent.get_inbox_report(max_emails=max_emails)


if __name__ == "__main__":
    app()
