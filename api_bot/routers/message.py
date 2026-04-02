from fastapi import APIRouter, status
from routers.base import handle_http_errors
from schemas.message import MessageAPICreate, MessageAPIResponse
from controllers.message import MessageLogic

router = APIRouter(prefix="/message", tags=["message"])


@router.post("/",
             response_model=MessageAPIResponse,
             status_code=status.HTTP_201_CREATED)
@handle_http_errors
async def create_user(data: MessageAPICreate):
    """Создание сообщения"""
    return MessageLogic.create(data)
