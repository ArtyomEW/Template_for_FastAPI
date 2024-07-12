from typing import Optional
from fastapi import Request, Depends
from fastapi_users import IntegerIDMixin, BaseUserManager, schemas, models, exceptions

from auth.utils import get_user_db
from models.model import User


SECRET = "SECRET"


# С помощью этой основной функции,мы можем управлять пользователями. Например отправлять смс на почту пользователя.
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    # Переменные для сбрасывания пароля
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    # Юзер менеджер управляет базой данных с пользователями.
    async def create(self, user_create: schemas.UC, safe: bool = False,
                     request: Optional[Request] = None, ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (user_create.create_update_dict() if safe else user_create.create_update_dict_superuser())

        # Тут алгоритм таков что поле которое мы передали в схеме как password, мы его переназначаем на Hashed_password

        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        # И мы также делаем с ролью, если юзер введёт свою выдуманную роль, то всё равно его роль будет по умолчанию
        # ссылаться на первую
        user_dict['role_id'] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
