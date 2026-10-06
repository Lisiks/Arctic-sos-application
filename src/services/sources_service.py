from fastapi import Depends
from typing import Annotated

from ..models.sources_models import SourceGetModel, SourcePostModel
from ..models.users_models import UserJWTModel
from ..database.repositories import SourcesRepository
from ..enums import UserRoles
from ..exceptions import IncorrectUserRole, NotFoundRecordException


class SourcesService:
    def __init__(self, repository: Annotated[SourcesRepository, Depends(SourcesRepository)]):
        self.__repository = repository


    async def create(self, source_params: SourcePostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(source_params)


    async def modify(self, source_id: int, source_params: SourcePostModel, auth_data: UserJWTModel)  -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.modify(source_id, source_params)


    async def make_checked(self, source_id: int, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.make_checked(source_id)


    async def delete(self, source_id: int, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.delete(source_id)


    async def get_by_id(self, source_id, auth_data: UserJWTModel) -> SourceGetModel:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        source = await self.__repository.get_by_id(source_id)

        if source is None:
            raise NotFoundRecordException("Crew doesn't found!")

        return source


    async def get_all(self, auth_data: UserJWTModel) -> list[SourcePostModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all()


