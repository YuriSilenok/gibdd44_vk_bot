import os

from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Optional

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Конфигурация - замените на свои значения
VK_SECRET = "ваш_секретный_ключ"          # Из настроек Callback API
VK_CONFIRMATION_CODE = "2beb67a4"  # Токен из настроек Callback API
VK_ACCESS_TOKEN = os.getenv("BOT_TOKEN")
API_VERSION = "5.199"

app = FastAPI()


class VKCallbackEvent(BaseModel):
    type: str
    object: dict
    group_id: int
    secret: Optional[str] = None


def send_vk_message(peer_id: int, text: str):
    """Отправляет сообщение в VK через API"""
    import requests
    params = {
        "access_token": VK_ACCESS_TOKEN,
        "v": API_VERSION,
        "peer_id": peer_id,
        "message": text,
        "random_id": 0
    }
    response = requests.post("https://api.vk.com/method/messages.send", params=params)
    return response.json()

@app.post("/callback")
async def vk_callback(request: Request):
    # Получаем сырые данные для проверки секрета
    body = await request.json()
    
    # Проверка секрета (опционально, но рекомендуется)
    if VK_SECRET and body.get("secret") != VK_SECRET:
        return Response(content="Wrong secret", status_code=403)
    
    event_type = body.get("type")
    
    # 1. Обработка подтверждения сервера
    if event_type == "confirmation":
        return Response(content=VK_CONFIRMATION_CODE, media_type="text/plain")
    
    # 2. Обработка новых сообщений
    if event_type == "message_new":
        message_obj = body.get("object", {})
        # Извлекаем текст и ID отправителя
        user_text = message_obj.get("message", {}).get("text")
        peer_id = message_obj.get("message", {}).get("peer_id")
        
        if user_text and peer_id:
            # Отправляем эхо-ответ
            send_vk_message(peer_id, f"Эхо: {user_text}")
        
        # VK ждет ответ 'ok' для остальных событий
        return Response(content="ok", media_type="text/plain")
    
    # Для всех остальных событий
    return Response(content="ok", media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)