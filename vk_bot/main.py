"""Модуль для запуска VK бота"""

import asyncio
from contextlib import asynccontextmanager
import os
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


@app.get("/")
async def root(request: Request):
    return {"ok": True}


class WebHook(BaseModel):
    type: Literal["text"]
    text: str


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    if data.get('type') == 'text':
        bot.api.messages.send(
            
        )
    return {"ok": True}


async def run_fastapi():
    config = uvicorn.Config(app, host="127.0.0.1", port=8012, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def run_bot():

    bot.run_forever()

async def main():
    await asyncio.gather(
        run_fastapi(),
        run_bot(),
        return_exceptions=True
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановка...")
