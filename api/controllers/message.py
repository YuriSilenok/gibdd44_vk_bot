from models import UserMessage, User
from schemas.message import MessageAPICreate, MessageAPIResponse


class MessageLogic:
    @classmethod
    def create(cls, data: MessageAPICreate):

        if data.type == 'text':
            user_message: UserMessage = UserMessage.create(
                from_user=User.get(
                    user_id=data.user.id,
                    type=data.user.type,
                ),
                type=data.type,
                text=data.text,
            )
        else:
            raise ValueError(f'Тип сообщения {data.type} не реализоан')

        message_api_response: MessageAPIResponse = MessageAPIResponse(
            **data.model_dump(),
            id=user_message.id,
        )

        return message_api_response
