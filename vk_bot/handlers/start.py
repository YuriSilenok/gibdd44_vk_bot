import aiohttp
from vkbottle import Keyboard, KeyboardButtonColor, Location
from vkbottle.bot import Message, BotLabeler
from vkbottle_types.objects import UsersUserFull
from config import url

labeler = BotLabeler()


def get_location_keyboard():
    """Клавиатура с кнопкой для отправки геолокации"""
    keyboard = (
        Keyboard(one_time=False)
        .add(Location(), color=KeyboardButtonColor.PRIMARY)
        .row()
    )
    return keyboard.get_json()


@labeler.message(text='Начать')
async def start_cmd(message: Message):
    await message.answer(
        "❗️Уважаемые участники дорожного движения!\n"
        "🚓Госавтоинспекция Костромской области информирует, что для "
        "предупреждения ДТП с участием нетрезвых водителей создан чат-бот "
        "📲\n 👉С его помощью можно анонимно сообщать о водителях "
        "с признаками опьянения, которые управляют транспортом.\n"
        "⛔️В сообщении необходимо указать информацию об автомобиле "
        "(номер, марка, цвет, направление движения), "
        "также можешь оставить геопозицию, прикрепить фото или видео.\n"
        "❗️Внимание вся поступившая информация обрабатывается роботом",
        keyboard=get_location_keyboard(),
    )

    user: UsersUserFull = await message.get_user()
    data = {
        "id": user.id,
        'type': 'vk',
        'user_vk': {
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}/user/", json=data) as response:
            result = await response.json()
            print(result)
