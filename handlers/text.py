from vk_bot import Router, Message, F

router = Router()


@router.message(F.text == 'Привет')
def get_text(message: Message):
    message.answer(
        text='Пока'
    )
