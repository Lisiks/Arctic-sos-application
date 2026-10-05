from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.operation_acts_models import OperationActGetModel, OperationActPostModel
from ..models.users_models import UserJWTModel
from ..services import OpeartionActService

router = APIRouter(prefix="/operationacts", tags=["Operation acts"])


@router.post("/{message_id}", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[OpeartionActService, Depends(OpeartionActService)],
    message_id: Annotated[int, Path(gt=0)],
    data: Annotated[OperationActPostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> dict[str, str]:
    await service.create(message_id, data, auth_data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OperationActGetModel])
async def get_all(
    service: Annotated[OpeartionActService, Depends(OpeartionActService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[Optional[int], Query(gt=0)] = 1,
) -> list[OperationActGetModel]:
    return await service.get_all(page, auth_data)