# sms_handler.py
from twilio.twiml.messaging_response import MessagingResponse

from services.chat_service import ChatService


class SMSHandler:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def handle_message(self, from_, body):
        response = MessagingResponse()
        message = response.message()

        # Command handling
        if body.strip().lower() == "/help":
            message.body("Commands: /help, /balance, /reset, /map, or chat")
        elif body.strip().lower() == "/balance":
            message.body("Your balance is $100.")  # Placeholder
        elif body.strip().lower() == "/reset":
            self.chat_service.reset_history(from_)
            message.body("Chat history reset.")
        elif body.strip().lower().startswith("/map"):
            try:
                _, start, _, end = body.lower().split()
                directions = (
                    f"Directions from {start} to {end}."  # Placeholder for actual directions
                )
                message.body(directions)
            except ValueError:
                message.body("Please specify the route as: /map [origin] to [destination]")
        else:
            response_text = self.chat_service.get_response(from_, body)
            message.body(response_text)

        return str(response)
