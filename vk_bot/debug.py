import aiohttp
import asyncio


async def send_post_request():
    url = "http://127.0.0.1:8012/text"
    data = {
        "type": "text",
        "text": "Привет, мир!"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            result = await response.json()
            print(f"Статус: {response.status}")
            print(f"Ответ: {result}")
            return result

asyncio.run(send_post_request())
