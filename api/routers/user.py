from fastapi import APIRouter, status
from .base import handle_http_errors
from schemas.user import UserAPICreate, UserAPIResponse
from controllers.user import UserLogic

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/",
             response_model=UserAPIResponse,
             status_code=status.HTTP_201_CREATED)
@handle_http_errors
async def create_user(data: UserAPICreate):
    """Создание нового пользователя"""
    return UserLogic.create(data)
