from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.sources_models import SourceGetModel, SourcePostModel
from ..shemas import Sources

class SourcesRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, source_params: SourcePostModel) -> None:
        source = Sources(**source_params.model_dump())
        self.__session.add(source)
        await self.__session.commit()


    async def delete(self, source_id: int) -> None:
        source = await self.__session.get(Sources, source_id)
        if source is not None:
            await self.__session.delete(source)
            await self.__session.commit()


    async def modify(self, source_id: int, source_params: SourcePostModel) -> None:
        source = await self.__session.get(Sources, source_id)
        if source is not None:
            for field, value in source_params.model_dump().items():
                setattr(source, field, value)
            await self.__session.commit()


    async def make_checked(self, source_id: int) -> None:
        source = await self.__session.get(Sources, source_id)
        if source is not None:
            source.need_check = False
            await self.__session.commit()


    async def get_by_id(self, source_id: int) -> SourceGetModel | None:
        source = await self.__session.get(Sources, source_id)
        return SourceGetModel.model_validate(source) if source is not None else None


    async def get_all(self) -> list[SourceGetModel]:
        stmt = select(Sources)
        sources = await self.__session.scalars(stmt)
        return [SourceGetModel.model_validate(source) for source in sources.all()]