from vkbottle.bot import Message, BotLabeler
from vkbottle.dispatch.rules.base import FuncRule


labeler = BotLabeler()


def has_geo(message: Message) -> bool:
    """Проверяет, есть ли в сообщении геолокация"""
    return message.geo is not None


@labeler.message(FuncRule(has_geo))
async def ask_location(message: Message):
    coordinates = message.geo.coordinates

    latitude = coordinates.latitude
    longitude = coordinates.longitude

    await message.answer(
        f"📍 Получены координаты!\n"
        f"Широта: {latitude}\n"
        f"Долгота: {longitude}"
    )
