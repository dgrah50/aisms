from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response

from app.api.security.twilio_validator import validate_twilio_request
from app.api.sms_handler import SMSHandler
from services.account_service import AccountService

router = APIRouter()


def get_sms_handler(request: Request):
    return request.app.state.sms_handler


@router.post("/register/")
async def register_number(
    PhoneNumber: str = Form(...),
    MessagesBought: int = Form(...),
):
    account = await AccountService.register_or_update_number(PhoneNumber, MessagesBought)
    return {
        "message": f"Number {account.phone_number} registered or updated successfully with message credits: {account.balance}"
    }


@router.post("/sms/")
async def receive_sms(
    # validated: bool = Depends(validate_twilio_request),
    From: str = Form(...),
    Body: str = Form(...),
    sms_handler: SMSHandler = Depends(get_sms_handler),
):
    # Check and decrement message count
    if not await AccountService.decrement_message_count(From):
        raise HTTPException(
            status_code=403, detail="Insufficient message credits or unauthorized number"
        )

    response_xml = sms_handler.handle_message(From, Body)
    return Response(content=response_xml, media_type="application/xml")
