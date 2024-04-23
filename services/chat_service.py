import uuid
from typing import Any, Dict, cast

from cacheing import TTLCache
from langchain.agents import AgentExecutor, BaseMultiActionAgent, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from models.models import Message

from .mapping_service import mapping_tools

BASE_PROMPT = """
You are an AI-powered assistant designed to communicate via SMS. Your primary goal is to provide timely and accurate information to users in a concise manner. Keep your responses brief, typically under 320 characters, to ensure they fit within two SMS messages whenever possible. Focus on delivering clear and direct answers without extraneous details or conversational fillers.

Respond promptly to user inquiries with relevant information.
Use simple, clear language that can be easily understood on small screens.
Prioritize direct answers or instructions; avoid open-ended responses.
When necessary, guide users on how to obtain more detailed information via links or additional resources.
Automate common tasks and provide instant solutions where applicable.
For travel directions, deliver the directions in a clear, step-by-step, turn-by-turn, bullet point format. Include explicit instructions for:
   - Exact bus numbers or train lines needed.
   - You MUST include Specific bus stops or train platforms to use.
   - You MUST include Departure times for public transport, and if there are any transfers, provide timing details.
   - Estimated time of arrival at each transfer point and final destination.
   - Landmarks or physical store signs to look for when making turns or exiting transportation.
For complex routes or safety concerns, offer alternative route suggestions if available.
Your functionality includes handling FAQs, providing directions from point A to point B using a provided directions API. You do not support voice calls or multimedia messages. Always request clarification if a query is ambiguous or incomplete.
"""
# Constants

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", BASE_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

TIMEOUT_PERIOD = 300  # 5 minutes in seconds
CACHE_SIZE = 1000


class ChatService:
    """Service to manage chat interactions using a language model agent with caching of user history and conversation IDs."""

    def __init__(self, timeout: int = TIMEOUT_PERIOD):
        """Initialize the chat service with a timeout for caching and set up the agent execution chain."""
        self.cache: TTLCache = TTLCache(capacity=CACHE_SIZE, ttl=timeout)
        self.output_parser: StrOutputParser = StrOutputParser()

        self.agent: BaseMultiActionAgent = cast(
            BaseMultiActionAgent, create_tool_calling_agent(ChatOpenAI(), mapping_tools, PROMPT)
        )
        self.agent_executor: AgentExecutor = AgentExecutor(
            agent=self.agent, tools=mapping_tools, verbose=True
        )

    async def get_response(self, user_id: str, query: str) -> str:
        """Retrieve the response from the agent based on the user's query and chat history."""
        session = self.cache.get(user_id, {"id": str(uuid.uuid4()), "history": []})

        # Save the human message to the database
        await Message.create(user_id=user_id, content=query, conversation_id=session["id"])

        try:
            response: Dict[str, Any] = self.agent_executor.invoke(
                {"chat_history": session["history"], "input": query}
            )
            response_text = response["output"]

            # Save the AI message to the database
            await Message.create(
                user_id=user_id, content=response_text, conversation_id=session["id"]
            )

            # Update chat history
            session["history"].extend(
                [
                    HumanMessage(content=query),
                    AIMessage(content=response_text),
                ]
            )

            # Update the cache with the new history
            self.cache[user_id] = session

            return response_text
        except Exception as e:
            print(f"Error in generating response: {e}")
            return "Sorry, I am unable to process your request right now."

    def reset_history(self, user_id: str):
        """Clear the chat history for the specified user."""
        if user_id in self.cache:
            self.cache.pop(user_id, None)
