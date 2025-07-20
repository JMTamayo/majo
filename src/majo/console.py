from datetime import datetime as dt

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class AgentConsole:
    console: Console

    def __init__(self):
        self.console = Console()

    def get_console(self) -> Console:
        """
        Get the console object.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            Console: The console object.
        """
        return self.console

    def request_user_input(self) -> str:
        """
        Request a message from the user.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            str: The user input.
        """

        query: str = self.get_console().input("[blue]> ").strip()
        return query

    def print_agent_response(self, message: str) -> None:
        """
        Print an agent response message to the console.

        Arguments:
            message (str): The message to print.

        Returns:
            None: The function does not return something directly, it prints the agent response message to the console.
        """

        timestamp: str = dt.now().strftime("%H:%M:%S")
        title = Text("Majo", style="magenta")
        subtitle = Text(timestamp, style="magenta")

        response_message = Text(f"\n{message}\n", style="white")
        self.get_console().print(
            Panel(
                response_message,
                title=title,
                subtitle=subtitle,
                title_align="left",
                subtitle_align="right",
                border_style="magenta",
                width=int(self.get_console().width * 0.8),
                expand=False,
            ),
            justify="right",
        )
        self.get_console().line()

    def print_user_request(self, message: str) -> None:
        """
        Print a user request message to the console.

        Arguments:
            message (str): The message to print.

        Returns:
            None: The function does not return something directly, it prints the user request message to the console.
        """

        width: int = int(self.get_console().width * 0.8) if len(message) >= 30 else 30
        expand: bool = False if len(message) >= 50 else True

        timestamp = dt.now().strftime("%H:%M:%S")
        title = Text("User ", style="blue")
        subtitle = Text(timestamp, style="blue")

        response_message = Text(f"\n{message}\n", style="white")
        self.get_console().print(
            Panel(
                response_message,
                title=title,
                subtitle=subtitle,
                title_align="left",
                subtitle_align="right",
                border_style="blue",
                width=width,
                expand=expand,
            ),
            justify="left",
        )
        self.get_console().line()

    def print_graph(self, graph: str) -> None:
        """
        Print a graph to the console.

        Arguments:
            graph (str): The graph to print.
        """

        title = Text("Agent Graph ", style="bright_blue")

        response_message = Text(f"\n{graph}\n", style="white")
        self.get_console().print(
            Panel(
                response_message,
                title=title,
                border_style="bright_blue",
                expand=True,
            ),
        )
        self.get_console().line()


def print_error(message: str) -> None:
    """
    Print an error message to the console.

    Arguments:
        message (str): The message to print.

    Returns:
        None: The function does not return anything, it prints the error message to the console.
    """
    console = Console()

    title = Text("⚠️  Error", style="red")

    error_message = Text(f"\n{message}\n", style="red")
    console.print(
        Panel(
            error_message,
            title=title,
            title_align="left",
            border_style="red",
            width=int(console.width * 0.8),
            expand=False,
        ),
        justify="left",
    )
