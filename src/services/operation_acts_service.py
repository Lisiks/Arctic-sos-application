from fastapi import Depends
from typing import Annotated

from ..models.operation_acts_models import OperationActGetModel, OperationActPostModel
from ..models.users_models import UserJWTModel
from ..database.repositories import OperationActRepository
from ..enums import UserRoles
from ..exceptions import IncorrectUserRole


class OpeartionActService:
    def __init__(self, repository: Annotated[OperationActRepository, Depends(OperationActRepository)]):
        self.__repository = repository

    async def create(self, message_id, act_params: OperationActPostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(message_id, act_params, auth_data.id)


    async def get_all(self, page: int, auth_data: UserJWTModel) -> list[OperationActGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all(page)