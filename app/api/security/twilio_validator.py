import os

from fastapi import Depends, Header, HTTPException, Request
from twilio.request_validator import RequestValidator

twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")


async def validate_twilio_request(request: Request, x_twilio_signature: str = Header(...)):
    validator = RequestValidator(twilio_auth_token)

    form_data = await request.form()
    url = str(request.url)

    if not validator.validate(url, form_data, x_twilio_signature):
        raise HTTPException(status_code=403, detail="Invalid request signature.")

    return True
