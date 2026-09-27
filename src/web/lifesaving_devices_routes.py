from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import LifesavingDevicesRepository
from ..models.lifesaving_devises_models import LivesavingDeviceGetModel, LivesavingDevicePostModel

router = APIRouter(prefix="/lifesavingdevices", tags=["Lifesaving devices"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
    data: Annotated[LivesavingDevicePostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(data)
    return {"msg": "created"}


@router.delete("/{device_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
    device_id: Annotated[int, Path(gt=0)]
) -> dict[str, str]:
    await repo.delete(device_id)
    return {"msg": "deleted"}


@router.patch("/{device_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
    device_id: Annotated[int, Path(gt=0)],
    data: Annotated[LivesavingDevicePostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.modify(device_id, data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LivesavingDeviceGetModel])
async def get_all(
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
) -> list[LivesavingDeviceGetModel]:
    return await repo.get_all()