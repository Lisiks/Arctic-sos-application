from fastapi import Depends
from typing import Annotated

from ..models.crews_models import CrewGetModel, CrewPostModel
from ..models.users_models import UserJWTModel
from ..database.repositories import CrewsRepository
from ..enums import Position, UserRoles
from ..exceptions import IncorrectUserRole, NotFoundRecordException


class CrewsService:
    def __init__(self, repository: Annotated[CrewsRepository, Depends(CrewsRepository)]):
        self.__repository = repository

    async def create(self, crew_params: CrewPostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(crew_params)

    async def modify(self, crew_id: int, crew_params: CrewPostModel, auth_data: UserJWTModel)  -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.modify(crew_id, crew_params)

    async def delete(self, crew_id: int, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.delete(crew_id)

    async def get_by_id(self, crew_id, auth_data: UserJWTModel) -> CrewGetModel:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        crew = await self.__repository.get_by_id(crew_id)

        if crew is None:
            raise NotFoundRecordException("Crew doesn't found!")

        return crew

    async def get_all(self, auth_data: UserJWTModel) -> list[CrewGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all()


