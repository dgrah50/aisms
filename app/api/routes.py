import os

from fastapi import APIRouter, Depends, Form, Request, Response

from app.api.security.twilio_validator import validate_twilio_request
from app.api.sms_handler import SMSHandler
from services.chat_service import ChatService
from utilities.utils import ConfigurationError

router = APIRouter()

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ConfigurationError("OPENAI_API_KEY is not defined in the environment variables.")

chat_service = ChatService()

sms_handler = SMSHandler(chat_service=chat_service)


@router.post("/sms/")
async def receive_sms(
    request: Request,
    validated: bool = Depends(validate_twilio_request),
    From: str = Form(...),  # Using `Form` to extract the sender's number from the request
    Body: str = Form(...),  # Using `Form` to extract the message body from the request
):
    """
    Endpoint to receive SMS messages and respond accordingly based on the content.
    """
    response_xml = await sms_handler.handle_message(From, Body)
    return Response(content=response_xml, media_type="application/xml")
