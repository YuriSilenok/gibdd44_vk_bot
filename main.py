import os

from api import app
from vk_bot import Bot
from dotenv import load_dotenv
from handlers import text

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

bot = Bot(token=TOKEN, group_id=GROUP_ID)
bot.include_router(text.router)

if __name__ == "__main__":
    bot.run(app)
