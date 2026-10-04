from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session

from ...models.crews_models import CrewGetModel, CrewPostModel
from ..shemas import Crews

class CrewsRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session

    async def create(self, crew_params: CrewPostModel) -> None:
        crew = Crews(**crew_params.model_dump())
        self.__session.add(crew)
        await self.__session.commit()

    async def delete(self, crew_id: int) -> None:
        crew = await self.__session.get(Crews, crew_id)

        if crew is not None:
            await self.__session.delete(crew)
            await self.__session.commit()

    async def modify(self, crew_id: int, crew_params: CrewPostModel) -> None:
        crew = await self.__session.get(Crews, crew_id)

        if crew is not None:
            for field, value in crew_params.model_dump().items():
                setattr(crew, field, value)

            await self.__session.commit()


    async def get_by_id(self, crew_id: int) -> CrewGetModel | None:
        stmt = select(Crews).options(joinedload(Crews.lifesaving_device)).where(Crews.id == crew_id)
        crew = await self.__session.scalar(stmt)
        return CrewGetModel.model_validate(crew) if crew is not None else None


    async def get_all(self) -> list[CrewGetModel]:
        stmt = select(Crews).options(joinedload(Crews.lifesaving_device))
        crews = await self.__session.scalars(stmt)

      
        return [CrewGetModel.model_validate(crew) for crew in crews.all()]

