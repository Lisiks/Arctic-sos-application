from fastapi import Depends
from typing import Annotated

from ..models.users_models import UserGetModel, UserPostModel, UserLoginModel, UserJWTModel
from ..database.repositories.users_repository import UsersRepository
from ..enums import UserRoles
from ..exceptions import IncorrectUserRole
from ..utils import JWTManager, PasswordManager

class UsersService:
    def __init__(self, repository: Annotated[UsersRepository, Depends(UsersRepository)]):
        self.__repository = repository

    async def create_user(self, user_params: UserPostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role != UserRoles.SUPERUSER:
            raise IncorrectUserRole("This function only for superuser!")

        user_params.password_hash = PasswordManager.hash_password(user_params.plain_password)
        await self.__repository.create_user(user_params)

    async def delete_user(self, user_id: int, auth_data: UserJWTModel) -> None:
        if auth_data.role != UserRoles.SUPERUSER:
            raise IncorrectUserRole("This function only for superuser!")

        delete_result = await self.__repository.delete_user(user_id)
        if delete_result:
            JWTManager.add_deleted_user_id(user_id)

    async def get_all(self, auth_data: UserJWTModel) -> list[UserGetModel]:
        if auth_data.role != UserRoles.SUPERUSER:
            raise IncorrectUserRole("This function only for superuser!")

        return await self.__repository.get_all()

    async def login_user(self, login_data: UserLoginModel) -> str:
        user = await self.__repository.login(login_data)
        return JWTManager.create_jwt(user)


