"""Модуль для базы данных"""

from datetime import datetime
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    BooleanField,
    FloatField,
)

# pylint: disable=R0903
DB = SqliteDatabase("sqlite.db")


class Table(Model):
    """Базовая модель"""

    class Meta:
        """Класс мета"""

        database = DB


class User(Table):
    """Класс пользователя"""

    user_id = IntegerField()
    type = CharField(max_length=3)
    at_created = DateTimeField(default=datetime.now)
    ban_count = IntegerField(default=0)
    ban_until = DateTimeField(null=True)

    class Meta:
        indexes = (
            # Создаем уникальный индекс для пары (id, type)
            (('user_id', 'type'), True),
        )


class UserVK(Table):
    user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    first_name = CharField(null=True)
    last_name = CharField(null=True)


class UserMAX(Table):
    user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")


class Role(Table):
    """Класс ролей"""

    name = CharField()


class UserRole(Table):
    """Класс роли пользователей"""

    user = ForeignKeyField(
        User, backref="user_roles", on_update="CASCADE", on_delete="CASCADE"
    )
    role = ForeignKeyField(
        Role, backref="role_users", on_update="CASCADE", on_delete="CASCADE"
    )


class Permition(Table):
    """Приведегия выданная"""

    name = CharField()


class RolePermition(Table):
    """Выданные привилегии для роли"""

    permition = ForeignKeyField(
        model=Permition, on_update="CASCADE", on_delete="CASCADE"
    )
    role = ForeignKeyField(Role, on_update="CASCADE", on_delete="CASCADE")


class MessageType(Table):
    """Тип сообщения"""

    name = CharField(max_length=10)


class UserMessage(Table):
    """Класс сообщений пользователя"""

    from_user: User = ForeignKeyField(
        model=User,
        on_update="CASCADE",
        on_delete="CASCADE",
    )
    type = ForeignKeyField(
        model=MessageType,
        on_update="CASCADE",
        on_delete="CASCADE",
    )
    text = CharField(max_length=4096, null=True)
    at_created = DateTimeField(default=datetime.now)


class ForwardMessage(Table):
    """Пересланое сообщение"""

    user_message = ForeignKeyField(
        model=UserMessage, on_update="CASCADE", on_delete="CASCADE"
    )
    to_user: User = ForeignKeyField(
        model=User,
        on_update="CASCADE",
        on_delete="CASCADE",
    )
    at_created = DateTimeField(default=datetime.now)
    tg_message_id = IntegerField()
    is_delete = BooleanField(default=False)


class Location(Table):
    """Класс для хранения геолокационных данных"""

    message = ForeignKeyField(
        model=UserMessage,
        backref="location",
        on_update="CASCADE",
        on_delete="CASCADE",
    )
    longitude = FloatField()
    latitude = FloatField()


class MessageFile(Table):
    """Сведения о видео"""

    message = ForeignKeyField(
        model=UserMessage,
        backref="file",
        on_update="CASCADE",
        on_delete="CASCADE",
    )
    file_id = CharField(max_length=128)


class Patrol(Table):
    """Класс для сообщения о выезде инспектора"""

    inspector = ForeignKeyField(
        User, backref="patrol", on_update="CASCADE", on_delete="CASCADE"
    )
    start = DateTimeField(default=datetime.now)
    end = DateTimeField(null=True)


class Admin(Table):
    """Класс для хранения настроек администратора"""

    user = ForeignKeyField(User, on_update="CASCADE", on_delete="CASCADE")
    is_notify = BooleanField(default=False)


def init_db():
    DB.connect()
    DB.create_tables(
        models=[
            User,
            UserVK,
            UserMAX,
            Role,
            UserRole,
            Permition,
            RolePermition,
            MessageType,
            UserMessage,
            ForwardMessage,
            Patrol,
            Admin,
            MessageFile,
            Location,
        ],
        safe=True,
    )
    DB.close()

    permitions = [
        "Начать патрулирование",
        "Закончить патрулирование",
        "Показать администраторов",
        "Добавить администратора",
        "Удалить роль администратора",
        "Показать инспекторов",
        "Добавить инспектора",
        "Удалить роль инспектора",
        "Получать сообщения очевидцев",
        "Не получать сообщения очевидцев",
        "Бан пользователя",
        "Показать информацию о пользователе",
        "Отправить сообщение",
    ]

    for permition in permitions:
        Permition.get_or_create(name=permition)

    roles = [
        "Начальник",
        "Администратор",
        "Инспектор",
        "Очевидец",
    ]

    for role in roles:
        Role.get_or_create(name=role)

    rolepermitions = [
        # Привелегии начальника
        ("Начальник", "Показать администраторов"),
        ("Начальник", "Добавить администратора"),
        ("Начальник", "Удалить роль администратора"),
        ("Начальник", "Показать инспекторов"),
        ("Начальник", "Добавить инспектора"),
        ("Начальник", "Удалить роль инспектора"),
        ("Начальник", "Показать информацию о пользователе"),
        ("Начальник", "Получать сообщения очевидцев"),
        ("Начальник", "Не получать сообщения очевидцев"),
        ("Начальник", "Бан пользователя"),
        # Привелегии администратора
        ("Администратор", "Показать администраторов"),
        ("Администратор", "Добавить администратора"),
        ("Администратор", "Показать инспекторов"),
        ("Администратор", "Добавить инспектора"),
        ("Администратор", "Удалить роль инспектора"),
        ("Администратор", "Показать информацию о пользователе"),
        ("Администратор", "Получать сообщения очевидцев"),
        ("Администратор", "Не получать сообщения очевидцев"),
        ("Администратор", "Бан пользователя"),
        # Привелегии инспектора
        ("Инспектор", "Начать патрулирование"),
        ("Инспектор", "Закончить патрулирование"),
        ("Инспектор", "Бан пользователя"),
        # Очевидец
        ("Очевидец", "Отправить сообщение"),
    ]

    for role, permition in rolepermitions:
        RolePermition.get_or_create(
            role=Role.get(name=role),
            permition=Permition.get(name=permition),
        )

    role: Role = Role.get(name="Очевидец")
    for user in User.select():
        UserRole.get_or_create(
            role=role,
            user=user,
        )

    messagetypes = ["text", "photo", "video", "location", "animation"]

    for messagetype in messagetypes:
        MessageType.get_or_create(name=messagetype)
