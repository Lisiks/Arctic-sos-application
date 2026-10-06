from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.lie_acts_models import LieActGetModel, LieActPostModel
from ..shemas import LieActs, HelpMessages

class LieActRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, message_id: int, lie_act_params: LieActPostModel, user_id: int) -> None:
        lie_act = LieActs(**lie_act_params.model_dump(), help_message_id=message_id, user_id=user_id)
        self.__session.add(lie_act)
        await self.__session.commit()


    async def get_all(self, page: int) -> list[LieActGetModel]:
        stmt = select(LieActs).options(
            joinedload(LieActs.help_message).joinedload(HelpMessages.source),
            joinedload(LieActs.user)
        ).order_by(desc(LieActs.fact_datetime),LieActs.help_message_id).limit(30).offset((page - 1) * 30)
        lie_acts = await self.__session.scalars(stmt)
        return [LieActGetModel.model_validate(lie_act) for lie_act in lie_acts.all()]