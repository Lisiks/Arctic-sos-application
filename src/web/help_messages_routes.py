from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional


from ..utils import auth
from ..models.users_models import UserJWTModel
from ..services import HelpMessageService
from ..models.help_messages_models import HelpMessageGetModel, HelpMessagePostModel

router = APIRouter(prefix="/messages", tags=["Help messages"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    data: Annotated[HelpMessagePostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> dict[str, str]:
    await service.create(data, auth_data)
    return {"msg": "created"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[HelpMessageGetModel])
async def get_all(
    service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[Optional[int], Query(gt=0)] = 1
    
) -> list[HelpMessageGetModel]:
    return await service.get_all(page, auth_data)