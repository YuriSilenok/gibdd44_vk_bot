from typing import Literal

from pydantic import BaseModel
from .user import UserAPI


class MessageAPI(BaseModel):
    """Базовая схема текстового сообщения"""
    user: UserAPI
    type: Literal["text"]
    text: str


class MessageAPICreate(MessageAPI):
    """Создание текстового сообщения"""
    pass


class MessageAPIResponse(MessageAPI):
    """Схема для ответа"""
    id: int
