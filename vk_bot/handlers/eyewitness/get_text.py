import aiohttp
from vkbottle.bot import Message, BotLabeler
from config import url
from .const import TEXT


labeler = BotLabeler()


@labeler.message()
async def get_text_handler(message: Message):
    await message.answer(TEXT)

    data = {
        "user": {
            "id": message.from_id,
            "type": "vk",
        },
        "type": "text",
        'text': message.text,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}/message/", json=data) as response:
            result = await response.json()
            print(result)
