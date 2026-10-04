from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import HelpMessagesRepository
from ..models.help_messages_models import HelpMessageGetModel, HelpMessagePostModel

router = APIRouter(prefix="/messages", tags=["Help messages"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    data: Annotated[HelpMessagePostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[HelpMessageGetModel])
async def get_all(
    repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    page: Annotated[Optional[int], Query(gt=0)] = 1,
) -> list[HelpMessageGetModel]:
    return await repo.get_all(page)