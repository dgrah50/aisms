from tortoise import fields
from tortoise.models import Model


class Account(Model):
    id = fields.IntField(pk=True)
    phone_number = fields.CharField(max_length=15, unique=True)
    balance = fields.IntField(default=0)


class Message(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=50)
    conversation_id = fields.CharField(max_length=100)  # To store unique conversation IDs
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
