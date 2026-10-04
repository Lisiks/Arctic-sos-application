from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import LieActRepository
from ..models.lie_acts_models import LieActGetModel, LieActPostModel

router = APIRouter(prefix="/lieacts", tags=["Lie acts"])


@router.post("/{message_id}", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    message_id: Annotated[int, Path(gt=0)],
    repo: Annotated[LieActRepository, Depends(LieActRepository)],
    data: Annotated[LieActPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(message_id, data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[LieActGetModel])
async def get_all(
    repo: Annotated[LieActRepository, Depends(LieActRepository)],
    page: Annotated[Optional[int], Query(ge=0)] = 0,
) -> list[LieActGetModel]:
    return await repo.get_all(page)