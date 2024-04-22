from fastapi import Depends, Form, HTTPException

from app.api.config import get_whitelisted_numbers


def is_whitelisted(
    From: str = Form(...), whitelisted_numbers: list = Depends(get_whitelisted_numbers)
):
    if From not in whitelisted_numbers:
        raise HTTPException(status_code=403, detail="Phone number not authorized.")
    return True
