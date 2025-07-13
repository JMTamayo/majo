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
            You are a personal assistant to manage a user's email and help them with their questions.

            Some examples of questions you can answer:
            - Do I have any emails from the company's CEO in my inbox?
            - How many emails do I have in my inbox and how many are unread?
            - Make me a summary of my emails in my inbox.
            - Have I received a response to any email from the marketing leader?

            # Instructions:
            - You must answer in the language in which the user asks you.
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

    def get_inbox_report(self, max_emails: int):
        human_message = HumanMessage(
            content=f"""
            # Goal:
            Generate a report of the emails in my inbox that I haven't yet read, organizing them by priority level, giving a brief summary of each email.

            # Prioritization Levels:
            - Urgent: Emails that require immediate attention.
                * Emails containing important requests with a deadline to give the response.
                * Emails mentioning work accidents.
                * Emails from a government entity.
            - Important: Emails that are important to read.
                * Emails from the Human Resources team mentioning topics related to personnel management.
                * Meeting requests.
                * Scheduled maintenance emails.
            - Unimportant: Emails that are not important to read with high priority but should be read some day.
                * Commercial offers, Newsletters or automatic emails from a business.

            # Rules:
            - The maximum number of emails to report is {max_emails}.
            """
        )

        input = {"messages": [human_message]}

        response = self.__get_agent().invoke(input=input)
        print(response["messages"][-1].content)
