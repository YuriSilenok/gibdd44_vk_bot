"""подключение роутеров"""

from vkbottle import Bot
from . import start
from . import eyewitness


def setup_labelers(bot: Bot):
    """Подключение роутеров"""
    bot.labeler.load(start.labeler)
    eyewitness.setup_labelers(bot=bot)
