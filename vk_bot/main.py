import asyncio
import os
import threading
from typing import List, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot import VKBot


env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = 236877722


bot = VKBot(token=TOKEN, group_id=GROUP_ID)
app = FastAPI()


@app.get("/")
async def root(request: Request):
    bot.send_message(
        user_id=146885046,
        text='text',
    )
    return {"ok": True}


class WebHook(BaseModel):
    type: Literal["text"]
    user_ids: List[int]
    text: str


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    return {"ok": True}


def run_fastapi():
    config = uvicorn.Config(app, host="127.0.0.1", port=8012, log_level="info")
    server = uvicorn.Server(config)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server.serve())


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    bot.run()