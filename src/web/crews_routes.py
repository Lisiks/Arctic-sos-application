from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.users_models import UserJWTModel
from ..services import CrewsService
from ..models.crews_models import CrewGetModel, CrewPostModel

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[CrewsService, Depends(CrewsService)],
    data: Annotated[CrewPostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.create(data, auth_data)
    return {"msg": "created"}


@router.delete("/{crew_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    service: Annotated[CrewsService, Depends(CrewsService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    crew_id: Annotated[int, Path(gt=0)]
) -> dict[str, str]:
    await service.delete(crew_id, auth_data)
    return {"msg": "deleted"}


@router.patch("/{crew_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    service: Annotated[CrewsService, Depends(CrewsService)],
    crew_id: Annotated[int, Path(gt=0)],
    data: Annotated[CrewPostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.modify(crew_id, data, auth_data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CrewGetModel])
async def get_all(
    service: Annotated[CrewsService, Depends(CrewsService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> list[CrewGetModel]:
    return await service.get_all(auth_data)