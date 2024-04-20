from tortoise import fields
from tortoise.models import Model


class Account(Model):
    id = fields.IntField(pk=True)
    phone_number = fields.CharField(max_length=15, unique=True)
    balance = fields.IntField(default=0)
