from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.users_models import UserJWTModel
from ..services import SourcesService
from ..models.sources_models import SourceGetModel, SourcePostModel

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[SourcesService, Depends(SourcesService)],
    data: Annotated[SourcePostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.create(data, auth_data)
    return {"msg": "created"}


@router.delete("/{source_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    service: Annotated[SourcesService, Depends(SourcesService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    source_id: Annotated[int, Path(gt=0)]
) -> dict[str, str]:
    await service.delete(source_id, auth_data)
    return {"msg": "deleted"}


@router.patch("/{source_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    service: Annotated[SourcesService, Depends(SourcesService)],
    source_id: Annotated[int, Path(gt=0)],
    data: Annotated[SourcePostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.modify(source_id, data, auth_data)
    return {"msg": "modified"}


@router.patch("/check/{source_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def make_check(
    service: Annotated[SourcesService, Depends(SourcesService)],
    source_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> dict[str, str]:
    await service.make_checked(source_id, auth_data)
    return {"msg": "checked"}
    


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[SourceGetModel])
async def get_all(
    service: Annotated[SourcesService, Depends(SourcesService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
) -> list[SourceGetModel]:
    return await service.get_all(auth_data)