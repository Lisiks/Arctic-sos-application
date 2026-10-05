from fastapi import Depends
from typing import Annotated

from ..database.repositories import LieActRepository
from ..models.lie_acts_models import LieActPostModel, LieActGetModel
from ..models.users_models import UserJWTModel
from ..enums import UserRoles
from ..exceptions import IncorrectUserRole


class LieActService:
    def __init__(self, repository: Annotated[LieActRepository, Depends(LieActRepository)]):
        self.__repository = repository

    async def create(self, message_id, act_params: LieActRepository, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(message_id, act_params)


    async def get_all(self, page: int, auth_data: UserJWTModel) -> list[LieActGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all(page)