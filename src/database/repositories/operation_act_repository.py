from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.operation_acts_models import OperationActGetModel, OperationActPostModel
from ..shemas import OperationActs, HelpMessages

class OperationActRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, message_id: int, operation_act_params: OperationActPostModel, user_id: int) -> None:
        operation_act = OperationActs(**operation_act_params.model_dump(), help_message_id=message_id, user_id=user_id)

        self.__session.add(operation_act)
        await self.__session.commit()


    async def get_all(self, page: int) -> list[OperationActGetModel]:
        stmt = select(
            OperationActs
        ).options(
            joinedload(OperationActs.help_message).joinedload(HelpMessages.source),
            joinedload(OperationActs.user)
        ).order_by(desc(OperationActs.fact_datetime), OperationActs.help_message_id).limit(30).offset((page - 1) * 30)
        operation_acts = await self.__session.scalars(stmt)
        return [OperationActGetModel.model_validate(operation) for operation in operation_acts.all()]