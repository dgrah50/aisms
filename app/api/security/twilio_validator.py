import os

from fastapi import Depends, Header, HTTPException, Request
from twilio.request_validator import RequestValidator

twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")


async def validate_twilio_request(
    request: Request,
    x_twilio_signature: str = Header(...),
    environment: str = Depends(lambda: os.getenv("ENVIRONMENT", "production")),
):
    # If the environment is not production, skip the actual validation
    if environment != "production":
        return True

    # Continue with validation if in production
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    validator = RequestValidator(twilio_auth_token)

    form_data = await request.form()
    url = str(request.url)

    if not validator.validate(url, form_data, x_twilio_signature):
        raise HTTPException(status_code=403, detail="Invalid request signature.")

    return True
