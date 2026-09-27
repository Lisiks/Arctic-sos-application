from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import OperationActRepository
from ..models.operation_acts_models import OperationActGetModel, OperationActPostModel

router = APIRouter(prefix="/operationacts", tags=["Operation acts"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    repo: Annotated[OperationActRepository, Depends(OperationActRepository)],
    data: Annotated[OperationActPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OperationActGetModel])
async def get_all(
    repo: Annotated[OperationActRepository, Depends(OperationActRepository)],
    page: Annotated[Optional[int], Query(ge=0)] = 0,
) -> list[OperationActGetModel]:
    return await repo.get_all(page)