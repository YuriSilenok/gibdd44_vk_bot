from models import User, UserVK
from schemas.user import UserAPICreate, UserAPIResponse, UserVKAPI


class UserLogic:
    @classmethod
    def create(cls, data: UserAPICreate):
        if data.type == 'vk' and not data.user_vk:
            raise ValueError(
                'Для типа пользоватея vk не заполнено поле user_vk'
            )

        if data.type != 'vk':
            raise ValueError(
                'Допустим только тип пользователя vk'
            )

        user: User
        user_vk: UserVK
        user, created = User.get_or_create(
            user_id=data.id,
            type=data.type,
        )

        user_api_response = UserAPIResponse(
            id=user.id,
            created=created,
            type=data.type,
        )

        if data.user_vk:
            user_vk: UserVK = UserVK.get_or_none(
                user=user
            )

            if user_vk is None:
                user_vk = UserVK.create(
                    user=user,
                    first_name=data.user_vk.first_name,
                    last_name=data.user_vk.last_name,
                )

            elif (
                user_vk.first_name != data.user_vk.first_name or
                user_vk.last_name != data.user_vk.last_name
            ):
                user_vk.first_name = data.user_vk.first_name
                user_vk.last_name = data.user_vk.last_name
                user_vk.save()

            user_api_response.user_vk = UserVKAPI(
                first_name=user_vk.first_name,
                last_name=user_vk.last_name,
            )

        return user_api_response
