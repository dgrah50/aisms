from datetime import datetime
from typing import Dict, List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    Represents a single message in a chat session.
    """

    text: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatSession(BaseModel):
    """
    Represents a chat session for a single user, containing all messages.
    """

    user_id: str
    messages: List[BaseMessage] = []

    def add_message(self, message: str):
        """
        Adds a new message to the chat session.
        """
        self.messages.append(HumanMessage(content=message))

    def clear_history(self):
        """
        Clears the message history of the chat session.
        """
        self.messages.clear()

    def get_messages(self):
        """
        Clears the message history of the chat session.
        """
        self.messages


class ChatHistory(BaseModel):
    """
    Holds chat sessions for all users, accessible by user ID.
    """

    sessions: Dict[str, ChatSession] = {}

    def get_session(self, user_id: str) -> ChatSession:
        """
        Retrieves the chat session for the specified user, creating a new session if it doesn't exist.
        """
        if user_id not in self.sessions:
            self.sessions[user_id] = ChatSession(user_id=user_id)
        return self.sessions[user_id]

    def clear_session(self, user_id: str):
        """
        Clears the chat history for the specified user.
        """
        if user_id in self.sessions:
            self.sessions[user_id].clear_history()
