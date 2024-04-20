import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.api.config import create_chat_service
from app.api.sms_handler import SMSHandler
from utilities.utils import get_database_url

load_dotenv()

TORTOISE_ORM = {
    "connections": {"default": get_database_url()},
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

from app.api.routes import router as sms_router  # noqa: E402

app = FastAPI()
app.include_router(sms_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    chat_service = create_chat_service()
    app.state.sms_handler = SMSHandler(chat_service=chat_service)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
