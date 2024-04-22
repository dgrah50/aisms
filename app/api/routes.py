from fastapi import APIRouter, Depends, Form, Request, Response

from app.api.security.twilio_validator import validate_twilio_request
from app.api.security.whitelisted_numbers import is_whitelisted
from app.api.sms_handler import SMSHandler

router = APIRouter()


def get_sms_handler(request: Request):
    return request.app.state.sms_handler


@router.post("/sms/")
async def receive_sms(
    validated: bool = Depends(validate_twilio_request),
    is_allowed: bool = Depends(is_whitelisted),
    From: str = Form(...),
    Body: str = Form(...),
    sms_handler: SMSHandler = Depends(get_sms_handler),
):
    response_xml = await sms_handler.handle_message(From, Body)
    return Response(content=response_xml, media_type="application/xml")
