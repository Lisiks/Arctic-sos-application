from fastapi import Depends
from typing import Annotated

from ..models.crews_models import CrewGetModel, CrewPostModel
from ..models.users_models import UserJWTModel
from ..database.repositories import HelpMessagesRepository
from ..enums import Position, UserRoles
from ..exceptions import IncorrectUserRole, NotFoundRecordException


class HelpMessageService:
    def __init__(self, repository: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)]):
        self.__repository = repository

    async def create(self, message_params: HelpMessagesRepository, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(message_params)


    async def get_by_id(self, message_id, auth_data: UserJWTModel) -> CrewGetModel:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        message = await self.__repository.get_by_id(message_id)

        if message is None:
            raise NotFoundRecordException("Message doesn't found!")

        return message

    async def get_all(self, page: int, auth_data: UserJWTModel) -> list[CrewGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all(page)


