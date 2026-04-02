"""Модуль для запуска VK бота"""

import asyncio
from contextlib import asynccontextmanager
import os
from typing import Literal
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from vkbottle import Bot
from handlers import setup_labelers

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
setup_labelers(bot=bot)


async def run_bot():
    bot.run_forever()


@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(bot.run_polling())

    yield

    polling_task.cancel()
    await asyncio.sleep(1)


app = FastAPI(lifespan=lifespan)


class WebHook(BaseModel):
    type: Literal["text"]
    text: str


@app.post("/text/")
async def root(webhook: WebHook):
    await bot.api.messages.send(
        user_id=146885046,
        message=webhook.text,
        random_id=0,
    )
    return {"webhook": webhook.model_dump()}
