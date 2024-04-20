import os

from services.chat_service import ChatService
from utilities.utils import ConfigurationError


def create_chat_service():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        raise ConfigurationError("OPENAI_API_KEY is not defined in the environment variables.")

    return ChatService()
