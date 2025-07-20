from pathlib import Path

from agent.agent import Majo
from config import EmailConfig, EmailProvider, LlmConfig, LlmProvider
from pydantic import SecretStr
from typer import Context, Option, Typer

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

    agent: Majo = Majo(llm_config=llm_config, email_config=email_config)

    ctx.meta["AGENT"] = agent


@app.command()
def ask(
    ctx: Context,
    question: str = Option(
        None,
        help="The question to ask Majo. You can use this option to make a simple one-shot question.",
    ),
    file: Path = Option(
        None,
        help="""
        The path to the file containing the question.
        You can use this option to pass a more complex question that you want to reuse in the future.
        """,
        exists=True,
        dir_okay=False,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Ask a question to Majo, your personal assistant.
    You can pass the question as an argument, a path to a file or make it interactively.
    """

    try:
        if question and file:
            raise ValueError(
                "You can only submit one of the arguments: a question or a file"
            )

        agent: Majo = ctx.meta["AGENT"]
        agent.ask(question or file)

    except KeyboardInterrupt:
        return


@app.command()
def graph(
    ctx: Context,
):
    """
    Print the graph of the agent.
    """

    agent: Majo = ctx.meta["AGENT"]
    agent.print_graph()


if __name__ == "__main__":
    app()
