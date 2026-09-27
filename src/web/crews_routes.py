from fastapi import APIRouter, Depends, status, Query, Form, Path
from typing import Annotated, Optional

from ..database.repositories import CrewsRepository
from ..models.crews_models import CrewGetModel, CrewPostModel, CrewGetModelWithLifesevingDevice

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    repo: Annotated[CrewsRepository, Depends(CrewsRepository)],
    data: Annotated[CrewPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.create(data)
    return {"msg": "created"}


@router.delete("/{crew_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    repo: Annotated[CrewsRepository, Depends(CrewsRepository)],
    crew_id: Annotated[int, Path(gt=0)]
) -> dict[str, str]:
    await repo.delete(crew_id)
    return {"msg": "deleted"}


@router.patch("/{crew_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def modify(
    repo: Annotated[CrewsRepository, Depends(CrewsRepository)],
    crew_id: Annotated[int, Path(gt=0)],
    data: Annotated[CrewPostModel, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await repo.modify(crew_id, data)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CrewGetModelWithLifesevingDevice])
async def get_all(
    repo: Annotated[CrewsRepository, Depends(CrewsRepository)],
) -> list[CrewGetModelWithLifesevingDevice]:
    return await repo.get_all()