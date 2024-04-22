# sms_handler.py
import logging

from twilio.twiml.messaging_response import MessagingResponse


class SMSHandler:
    def __init__(self, chat_service):
        self.chat_service = chat_service

    async def handle_message(self, from_, body):
        response = MessagingResponse()
        message = response.message()

        try:
            command = body.strip().lower()

            if command == "/help":
                message.body("Commands: /help, /reset, /map, or chat")
            elif command == "/reset":
                self.chat_service.reset_history(from_)
                message.body("Chat history reset.")
            else:
                response_text = await self.chat_service.get_response(from_, body)
                message.body(response_text)

        except Exception as e:
            logging.error(f"Error handling message from {from_}: {str(e)}")
            message.body("Error processing your request.")

        return str(response)
