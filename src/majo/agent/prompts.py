from typing import List

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage


class PromptBuilder:
    """
    A prompts builder for the email agent.
    """

    system_message: SystemMessage

    def __init__(self):
        system_message = SystemMessage(
            content="""
            # Role:
            You are a personal assistant to manage a user's email and help them with their questions. Your name is Majo.

            Some examples of questions you can answer:
            - Do I have any emails from the company's CEO in my inbox?
            - How many emails do I have in my inbox and how many are unread?
            - Make me a summary of my emails in my inbox.
            - Have I received a response to any email from the marketing leader?

            # Instructions:
            - You must answer in the language mentioned in the query. If not mentioned, you should answer in English.
            - You should always respond in a youthful and empathetic manner, so that people feel comfortable talking to you.
            - Use emojis to express your emotions and generate friendlier responses from people, but don't overdo it.
            - If you do not have the tools and information to answer the question, you should say the reason.
            - If the question is not related to the user's email service or generic information about email services, you should not answer it for any reason.
            - If the user's question contains offensive, racist, discriminatory or violent language, you should not answer the question for any reason.
            - You should not expose sensitive personal information such as addresses, passwords, account numbers, or phone numbers.
            """
        )

        self.system_message = system_message

    def get_system_message(self) -> SystemMessage:
        """
        Get the system message.

        Arguments:
            None: The function does not take any arguments.

        Returns:
            SystemMessage: The system message.
        """

        return self.system_message

    def build_detect_user_language_prompt(self, user_query: str) -> List[AnyMessage]:
        """
        Build a prompt to detect the language of the user's query.

        Arguments:
            user_query (str): The user's query.

        Returns:
            List[AnyMessage]: The prompt to detect the language of the user's query.
        """

        return [
            HumanMessage(
                content=f"""
                Detect the language of the user's query. Respond with a single word representing the language, for example: 'English', 'Spanish', 'French', etc.
                
                The user's query is:
                {user_query}
                """
            )
        ]

    def build_user_query_prompt(
        self, user_query: str, user_language: str | None = None
    ) -> List[AnyMessage]:
        """
        Build a prompt to ask the user's query.

        Arguments:
            user_query (str): The user's query.
            user_language (str | None): The language of the user's query.

        Returns:
            List[AnyMessage]: The prompt to ask the user's query.
        """

        human_message: HumanMessage = HumanMessage(
            content=user_query.strip(), additional_kwargs={"language": user_language}
        )
        return [self.get_system_message(), human_message]
