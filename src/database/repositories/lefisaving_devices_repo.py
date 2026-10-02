from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.lifesaving_devises_models import LivesavingDeviceGetModel, LivesavingDevicePostModel
from ..shemas import LifesavingDevices

class LifesavingDevicesRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session

    async def create(self, device_params: LivesavingDevicePostModel) -> None:
        device = LifesavingDevices(**device_params.model_dump())
        self.__session.add(device)
        await self.__session.commit()

    async def delete(self, device_id: int) -> None:
        device = await self.__session.get(LifesavingDevices, device_id)

        if device is not None:
            await self.__session.delete(device)
            await self.__session.commit()

    async def modify(self, device_id: int, device_params: LivesavingDevicePostModel) -> None:
        device = await self.__session.get(LifesavingDevices, device_id)

        if device is not None:
            for field, value in device_params.model_dump().items():
                setattr(device, field, value)

            await self.__session.commit()

    async def get_by_id(self, device_id: int) -> LivesavingDeviceGetModel | None:
        device = await self.__session.get(LifesavingDevices, device_id)
        return LivesavingDeviceGetModel.model_validate(device) if device is not None else None

    async def get_all(self) -> list[LivesavingDeviceGetModel]:
        stmt = select(LifesavingDevices)
        devices = await self.__session.scalars(stmt)
        return [LivesavingDeviceGetModel.model_validate(device) for device in devices.all()]