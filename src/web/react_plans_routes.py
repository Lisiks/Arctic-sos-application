from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..utils import auth
from ..models.users_models import UserJWTModel
from ..services import ReactionPlanService
from ..models.reaction_plans_models import ReactionPlanHistoryGetModel, ReactionPlanPostModel, ReactionPlanGetModel

router = APIRouter(prefix="/plans", tags=["Reaction plans"])


@router.post("/{message_id}", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    data: Annotated[ReactionPlanPostModel, Form(media_type="application/x-www-form-urlencoded")],
    message_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> dict[str, str]:
    await service.create(message_id, data, auth_data)
    return {"msg": "created"}


@router.patch("/{message_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    data: Annotated[ReactionPlanPostModel, Form(media_type="application/x-www-form-urlencoded")],
    message_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)]
) -> dict[str, str]:
    await service.modify(message_id, data, auth_data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ReactionPlanGetModel])
async def get_all(
    service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[Optional[int], Query(gt=0)] = 1,
) -> list[ReactionPlanGetModel]:
    return await service.get_all(page, auth_data)


@router.get("/{message_id}/history", status_code=status.HTTP_200_OK, response_model=list[ReactionPlanHistoryGetModel])
async def get_all(
    service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    message_id: Annotated[int, Path(gt=0)]
) -> list[ReactionPlanGetModel]:
    return await service.get_history(message_id, auth_data)