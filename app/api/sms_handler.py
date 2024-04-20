# sms_handler.py
import logging

from twilio.twiml.messaging_response import MessagingResponse

from services.account_service import AccountService


class SMSHandler:
    def __init__(self, chat_service):
        self.chat_service = chat_service

    def handle_message(self, from_, body):
        response = MessagingResponse()
        message = response.message()

        try:
            command = body.strip().lower()

            if command == "/help":
                message.body("Commands: /help, /balance, /reset, /map, or chat")
            elif command == "/balance":
                balance = self._get_balance(from_)
                message.body(f"Your balance is ${balance}.")
            elif command == "/reset":
                self.chat_service.reset_history(from_)
                message.body("Chat history reset.")
            else:
                response_text = self.chat_service.get_response(from_, body)
                message.body(response_text)

        except Exception as e:
            logging.error(f"Error handling message from {from_}: {str(e)}")
            message.body("Error processing your request.")

        return str(response)

    async def _get_balance(self, phone_number):
        """
        Retrieves the balance for a specified phone number using the AccountService.

        Args:
            phone_number (str): The phone number associated with the account.

        Returns:
            int: The balance of messages available.
        """
        return await AccountService.get_balance(phone_number)
