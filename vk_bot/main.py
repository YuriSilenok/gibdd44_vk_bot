"""Модуль для запуска VK бота"""

import asyncio
from contextlib import asynccontextmanager
import os
import threading
from typing import Literal, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from vkbottle import Bot
from handlers import setup_labelers

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
setup_labelers(bot=bot)


app = FastAPI()


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
setup_labelers(bot=bot)



@app.get("/")
async def root(request: Request):
    await bot.api.messages.send(
        user_id=146885046,
        text='text',
    )
    return {"ok": True}



class WebHook(BaseModel):
    type: Literal["text"]
    text: str


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    return {"ok": data}


def run_fastapi():
    config = uvicorn.Config(app, host="127.0.0.1", port=8012, log_level="info")
    server = uvicorn.Server(config)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    try:
        fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
        fastapi_thread.start()
        bot.run_forever()
    except KeyboardInterrupt:
        print("Остановка...")
