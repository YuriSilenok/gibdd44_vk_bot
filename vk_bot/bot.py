import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class VKBot:
    def __init__(self, token:str, group_id: int):
        self.token = token
        self.group_id = group_id
        self.handlers = []

        self.session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.session, group_id)
        self.vk = self.session.get_api()

    
    def send_message(self, user_id: int, text: str):
        self.vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(0, 1000),
        )

    def registration_handler(self, method, filter: dict):
        self.handlers.append((method, filter))

    def run(self):
        print("Бот запущен и ожидает сообщения...")
        for event in self.longpoll.listen():
            pass