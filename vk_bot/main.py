"""Модуль для запуска VK бота"""

import os
from dotenv import load_dotenv
from vkbottle import Bot
from handlers import setup_labelers

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
setup_labelers(bot=bot)


if __name__ == "__main__":
    print("Бот запущен")
    bot.run_forever()
