from fastapi import HTTPException
from pydantic import validator
from pydantic.main import BaseModel
from tortoise.models import Model
from tortoise import fields


class Message(Model):
    id_message = fields.IntField(pk=True)
    message_text = fields.CharField(160)
    view_counter = fields.IntField()


class MessageRequestDto(BaseModel):
    message_text: str

    @validator('message_text', pre=True)
    def message_text_validator(cls, message_text):
        if len(str(message_text).strip(' ')) != 0:
            return message_text
        else:
            raise HTTPException(detail=f'invalid input: message cannot be empty', status_code=400)
