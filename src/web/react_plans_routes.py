from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import ReactPlansRepository
from ..models.reaction_plans_models import ReactionPlanHistoryGetModel, ReactionPlanPostModel, ReactionPlanGetModel

router = APIRouter(prefix="/plans", tags=["Reaction plans"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    data: Annotated[ReactionPlanPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(data)
    return {"msg": "created"}


@router.patch("/", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    data: Annotated[ReactionPlanPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.modify(data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ReactionPlanGetModel])
async def get_all(
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    page: Annotated[Optional[int], Query(ge=0)] = 0,
) -> list[ReactionPlanGetModel]:
    return await repo.get_all(page)


@router.get("/{help_message_id}/history", status_code=status.HTTP_200_OK, response_model=list[ReactionPlanHistoryGetModel])
async def get_all(
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    help_message_id: Annotated[int, Path(gt=0)]
) -> list[ReactionPlanGetModel]:
    return await repo.get_history(help_message_id)