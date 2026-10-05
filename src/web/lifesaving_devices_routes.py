from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.users_models import UserJWTModel
from ..services import LifesavingDeviceService
from ..models.lifesaving_devises_models import LivesavingDeviceGetModel, LivesavingDevicePostModel

router = APIRouter(prefix="/lifesavingdevices", tags=["Lifesaving devices"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    data: Annotated[LivesavingDevicePostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.create(data, auth_data)
    return {"msg": "created"}


@router.delete("/{device_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    device_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.delete(device_id, auth_data)
    return {"msg": "deleted"}


@router.patch("/{device_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    device_id: Annotated[int, Path(gt=0)],
    data: Annotated[LivesavingDevicePostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.modify(device_id, data, auth_data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LivesavingDeviceGetModel])
async def get_all(
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> list[LivesavingDeviceGetModel]:
    return await service.get_all(auth_data)