from fastapi import Depends
from typing import Annotated

from ..models.lifesaving_devises_models import LivesavingDeviceGetModel, LivesavingDevicePostModel
from ..models.users_models import UserJWTModel
from ..database.repositories import LifesavingDevicesRepository
from ..enums import Position, UserRoles
from ..exceptions import IncorrectUserRole, NotFoundRecordException


class LifesavingDeviceService:
    def __init__(self, repository: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)]):
        self.__repository = repository

    async def create(self, device_params: LivesavingDevicePostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(device_params)

    async def modify(self, device_id: int, device_params: LivesavingDevicePostModel, auth_data: UserJWTModel)  -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.modify(device_id, device_params)

    async def delete(self, device_id: int, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.delete(device_id)

    async def get_by_id(self, device_id, auth_data: UserJWTModel) -> LivesavingDeviceGetModel:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        device = await self.__repository.get_by_id(device_id)

        if device is None:
            raise NotFoundRecordException("Device doesn't found!")

        return device

    async def get_all(self, auth_data: UserJWTModel) -> list[LivesavingDeviceGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all()


