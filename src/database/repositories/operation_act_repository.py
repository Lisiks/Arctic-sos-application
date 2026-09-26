from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.operation_acts_models import OperationActGetModel, OperationActPostModel
from ..shemas import OperationActs

class OperationActRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, operation_act_params: OperationActPostModel) -> None:
        operation_act = OperationActs(**operation_act_params.model_dump())
        self.__session.add(operation_act)
        await self.__session.commit()


    async def get_all(self, page: int) -> list[OperationActGetModel]:
        stmt = select(OperationActs).options(joinedload(OperationActs.help_message)).order_by(OperationActs.help_message_id).limit(30).offset(page * 30)
        operation_acts = await self.__session.scalars(stmt)
        return [OperationActGetModel.model_validate(operation) for operation in operation_acts.all()]