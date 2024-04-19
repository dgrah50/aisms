from typing import cast

from cacheing import TTLCache
from langchain import hub
from langchain.agents import AgentExecutor, BaseMultiActionAgent, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from .mapping_service import mapping_tools

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")

TIMEOUT_PERIOD = 300  # 5 minutes (300 seconds)
CACHE_SIZE = 1000  # Adjust cache size as needed

agent = cast(BaseMultiActionAgent, create_tool_calling_agent(ChatOpenAI(), mapping_tools, prompt))


class ChatService:
    def __init__(self, timeout: int = 600):
        self.cache = TTLCache(capacity=CACHE_SIZE, ttl=timeout)
        self.output_parser = StrOutputParser()
        self.chain = AgentExecutor(agent=agent, tools=mapping_tools, verbose=True)

    def get_response(self, user_id: str, query: str) -> str:
        user_history = self.cache.get(user_id, [])
        print(user_history)
        try:
            response = self.chain.invoke({"chat_history": user_history, "input": query})
            user_history.extend(
                [
                    HumanMessage(content=query),
                    AIMessage(content=response["output"]),
                ]
            )
            self.cache[user_id] = user_history

            return str(response["output"])
        except Exception as e:
            print(f"Error in generating response: {e}")
            return "Sorry, I am unable to process your request right now."

    def reset_history(self, user_id: str):
        self.cache.delete(user_id)
