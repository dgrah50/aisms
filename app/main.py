from dotenv import load_dotenv

load_dotenv()

import uvicorn  # noqa: E402
from fastapi import FastAPI  # noqa: E402

from app.api.routes import router as sms_router  # noqa: E402

app = FastAPI()
app.include_router(sms_router)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
