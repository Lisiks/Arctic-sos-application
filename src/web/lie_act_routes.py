from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.lie_acts_models import LieActGetModel, LieActPostModel
from ..models.users_models import UserJWTModel
from ..services import LieActService

router = APIRouter(prefix="/lieacts", tags=["Lie acts"])


@router.post("/{message_id}", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[LieActService, Depends(LieActService)],
    message_id: Annotated[int, Path(gt=0)],
    data: Annotated[LieActPostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> dict[str, str]:
    await service.create(message_id, data, auth_data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LieActGetModel])
async def get_all(
    service: Annotated[LieActService, Depends(LieActService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[Optional[int], Query(gt=0)] = 1,
) -> list[LieActGetModel]:
    return await service.get_all(page, auth_data)