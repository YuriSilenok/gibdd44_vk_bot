from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Literal

from vk_bot import Bot


app = FastAPI()


class WebHook(BaseModel):
    type: Literal["text"]
    user_ids: List[int]
    text: str


@app.get("/")
async def root(request: Request):
    bot = Bot.get_instance()
    bot.send_message(
        user_id=146885046,
        text='test',
    )
    return {"ok": True}
