from enum import StrEnum
from pathlib import Path
from typing import Literal

from agent.prompts import PromptBuilder
from config import EmailConfig, LlmConfig
from console import AgentConsole
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import MessagesState, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command


class AgentState(MessagesState):
    """
    Represents the state of the agent to be used in the workflow.
    """

    user_language: str | None


class Nodes(StrEnum):
    """
    Represents the implemented nodes of the workflow.
    """

    START = "Identify user language"
    AGENT = "Email agent"


class Majo:
    """
    The email agent.
    """

    prompt_builder: PromptBuilder

    llm: BaseChatModel
    workflow: CompiledStateGraph

    console: AgentConsole

    def __init__(self, llm_config: LlmConfig, email_config: EmailConfig):
        llm: BaseChatModel = init_chat_model(
            model=llm_config.MODEL,
            model_provider=llm_config.PROVIDER.value,
            temperature=llm_config.TEMPERATURE,
            api_key=llm_config.API_KEY.get_secret_value(),
        )

        graph_builder = StateGraph(AgentState)
        graph_builder.add_node(Nodes.START, self.node_start)
        graph_builder.add_node(Nodes.AGENT, self.node_agent)

        graph_builder.add_edge(Nodes.START, Nodes.AGENT)

        graph_builder.set_entry_point(Nodes.START)

        workflow = graph_builder.compile()

        self.prompt_builder = PromptBuilder()
        self.llm = llm
        self.workflow = workflow
        self.console = AgentConsole()

    def get_prompt_builder(self) -> PromptBuilder:
        """
        Get the prompt builder, used to build the prompts for the LLM.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            PromptBuilder: The prompt builder.
        """

        return self.prompt_builder

    def get_llm(self) -> BaseChatModel:
        """
        Get the LLM, used to generate the responses.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            BaseChatModel: The LLM.
        """

        return self.llm

    def get_workflow(self) -> CompiledStateGraph:
        """
        Get the agent workflow

        Arguments:
            None: The function does not take any arguments.

        Returns:
            CompiledStateGraph: The agent workflow.
        """

        return self.workflow

    def get_console(self) -> AgentConsole:
        """
        Get the console, used to print the messages to the user.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            AgentConsole: The console.
        """

        return self.console

    def node_start(self, state: AgentState) -> Command[Literal[Nodes.AGENT]]:
        """
        The start node of the workflow.

        Arguments:
            state (AgentState): The state of the agent.

        Returns:
            Command[Literal[Nodes.AGENT]]: The command to go to the agent node.
        """

        response: BaseMessage = self.get_llm().invoke(
            self.get_prompt_builder().build_detect_user_language_prompt(
                str(state["messages"][-1].content)
            )
        )
        state["user_language"] = str(response.content)
        return Command(goto=Nodes.AGENT)

    def node_agent(self, state: AgentState) -> AgentState:
        """
        The agent node of the workflow, when the LLM thinks to answer the user's query.

        Arguments:
            state (AgentState): The state of the agent.

        Returns:
            AgentState: The state of the agent.
        """

        response: BaseMessage = self.get_llm().invoke(
            self.get_prompt_builder().build_user_query_prompt(
                str(state["messages"][-1].content),
            )
        )

        if isinstance(response, AIMessage):
            state["messages"].append(response)
        else:
            ai_message = AIMessage(content=response.content)
            state["messages"].append(ai_message)

        return state

    def print_graph(self) -> None:
        """
        Print the graph of the agent.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            None: The function does not return anything, it prints the graph to the console.
        """

        self.get_console().print_graph(self.get_workflow().get_graph().draw_ascii())

    def ask(self, human_input: str | Path | None):
        """
        Ask a question to the agent.

        Arguments:
            human_input (str | Path | None): The human input.

        Returns:
            None: The function does not return anything, it prints the messages to the user.
        """

        if isinstance(human_input, str):
            query = human_input.strip()
        elif isinstance(human_input, Path):
            query = human_input.read_text().strip()
        else:
            query = self.get_console().request_user_input()

        state = {"messages": self.get_prompt_builder().build_user_query_prompt(query)}
        events = self.get_workflow().stream(state, stream_mode="values")

        for event in events:
            message = event["messages"][-1]
            if isinstance(message, HumanMessage):
                self.get_console().print_user_request(str(message.content))
            else:
                self.get_console().print_agent_response(str(message.content))

        self.print_graph()
