from pydantic import BaseModel
from typing import Literal
from typing import Optional


class UserAPI(BaseModel):
    """Базовая схема пользователя"""
    id: int
    type: Literal['vk', 'max']


class UserVKAPI(BaseModel):
    """Информация о пользователе вк"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserAPICreate(UserAPI):
    """Создание пользователя"""
    user_vk: Optional[UserVKAPI] = None


class UserAPIResponse(UserAPI):
    """Схема для ответа"""
    user_vk: Optional[UserVKAPI] = None
    created: bool
