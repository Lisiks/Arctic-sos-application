from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.help_messages_models import HelpMessageGetModel, HelpMessagePostModel
from ..shemas import HelpMessages
from ...enums import IncidentStatus

class HelpMessagesRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, message_params: HelpMessagePostModel, user_id: int) -> None:
        message = HelpMessages(**message_params.model_dump(), status=IncidentStatus.ACCEPTED, user_id=user_id)
        self.__session.add(message)
        await self.__session.commit()

    async def get_by_id(self, message_id) -> HelpMessageGetModel | None:
        stmt = select(HelpMessages).options(joinedload(HelpMessages.source), joinedload(HelpMessages.user)).where(HelpMessages.id == message_id)
        message = await self.__session.scalar(stmt)
        return HelpMessageGetModel.model_validate(message) if message is not None else None


    async def get_all(self, page: int) -> list[HelpMessageGetModel]:
        stmt = select(HelpMessages).options(joinedload(HelpMessages.source), joinedload(HelpMessages.user)).order_by(desc(HelpMessages.datetime), HelpMessages.id).limit(30).offset((page - 1) * 30)
        messages = await self.__session.scalars(stmt)
        return [HelpMessageGetModel.model_validate(message) for message in messages.all()]
