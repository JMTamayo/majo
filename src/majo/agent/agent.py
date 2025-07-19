from langchain_core.language_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from config import LlmConfig
from agent.llms import LLM


class Majo:
    __agent: CompiledStateGraph

    def __init__(self, llm_config: LlmConfig):
        llm: BaseChatModel = LLM(config=llm_config).get_model()

        system_prompt: SystemMessage = SystemMessage(
            content="""
            # Role:
            You are a personal assistant to manage a user's email and help them with their questions. Your name is Majo.

            Some examples of questions you can answer:
            - Do I have any emails from the company's CEO in my inbox?
            - How many emails do I have in my inbox and how many are unread?
            - Make me a summary of my emails in my inbox.
            - Have I received a response to any email from the marketing leader?

            # Instructions:
            - You must answer in the language in which the user asks you.
            - You should always respond in a youthful and empathetic manner, so that people feel comfortable talking to you.
            - Use emojis to express your emotions and generate friendlier responses for people.
            - If you do not have the tools and information to answer the question, you should say the reason.
            - If the question is not related to the user's email service, you should not answer it for any reason.
            - If the user's question contains offensive, racist, discriminatory or violent language, you should not answer the question for any reason.
            - You should not expose sensitive personal information such as addresses, passwords, account numbers, or phone numbers.
            """
        )

        agent: CompiledStateGraph = create_react_agent(
            model=llm,
            tools=[],
            prompt=system_prompt,
        )

        self.__agent = agent

    def __get_agent(self) -> CompiledStateGraph:
        return self.__agent

    def ask(self, question: str) -> str:
        human_message = HumanMessage(content=question)
        input = {"messages": [human_message]}
        response = self.__get_agent().invoke(input=input)
        return response["messages"][-1].content
