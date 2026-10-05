from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...core import config
from ..shemas import Users
from ...models.users_models import UserGetModel, UserPostModel, UserLoginModel
from ...exceptions import FailedLoginException, DeleteSuperuserException
from ...utils import PasswordManager
from ...enums import UserRoles

class UsersRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session

    async def create_user(self, user_params: UserPostModel) -> None:
        user = Users(**user_params.model_dump())
        self.__session.add(user)
        await self.__session.commit()

    async def delete_user(self, user_id: int) -> bool:
        user = await self.__session.get(Users, user_id)

        if user is None:
            return False

        if user.role == UserRoles.SUPERUSER:
            raise DeleteSuperuserException("You cannot delete superuser!")

        await self.__session.delete(user)
        await self.__session.commit()
        return True

    async def get_all(self) -> list[UserGetModel]:
        stmt = select(Users)
        users = await self.__session.scalars(stmt)
        return [UserGetModel.model_validate(user) for user in users.all()]

    async def login(self, user_data: UserLoginModel) -> UserGetModel:
        stmt = select(Users).where(Users.username == user_data.username)
        user = await self.__session.scalar(stmt)

        if user is None or not PasswordManager.verify_password(user_data.plain_password, user.password_hash):
            raise FailedLoginException("Incorrect user or password!")

        return UserGetModel.model_validate(user)

    async def create_superuser(self) -> None:

        stmt = select(Users).where(Users.username == config.app.superuser_name)
        superuser = await self.__session.scalar(stmt)

        if superuser is None:
            superuser = Users(
                username=config.app.superuser_name,
                hash_password = PasswordManager.hash_password(config.app.superuser_password),
                role=UserRoles.SUPERUSER
            )
            self.__session.add(superuser)
        else:
            superuser.password_hash = PasswordManager.hash_password(config.app.superuser_password)
            
        await self.__session.commit()

    