"""подключение роутеров"""

from vkbottle import Bot
from . import get_location
from . import get_text


def setup_labelers(bot: Bot):
    """Подключение роутеров"""
    bot.labeler.load(get_location.labeler)
    bot.labeler.load(get_text.labeler)
