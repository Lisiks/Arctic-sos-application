from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session
from ...models.reaction_plans_models import ReactionPlanGetModel, ReactionPlanPostModel, ReactionPlanHistoryGetModel
from ..shemas import ReactionPlans, ReactionPlansHistory


class ReactPlansRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, plan_params: ReactionPlanPostModel) -> None:
        plan = ReactionPlans(**plan_params.model_dump())
        self.__session.add(plan)
        await self.__session.commit()


    async def modify(self, plan_params: ReactionPlanPostModel) -> None:
        plan = await self.__session.get(ReactionPlans, plan_params.help_message_id)

        if plan is not None:
            for field, value in plan_params.model_dump().items():
                setattr(plan, field, value)
                await self.__session.commit()


    async def get_all(self, page: int) -> list[ReactionPlanGetModel]:
        stmt = select(ReactionPlans).options(joinedload(ReactionPlans.lifesaving_device), joinedload(ReactionPlans.help_message)).order_by(ReactionPlans.help_message_id).limit(30).offset(page * 30)
        plans = await self.__session.scalars(stmt)
        return [ReactionPlanGetModel.model_validate(plan) for plan in plans.all()]


    async def get_history(self, help_message_id: int) -> list[ReactionPlanHistoryGetModel]:
        stmt = select(ReactionPlansHistory).options(joinedload(ReactionPlansHistory.lifesaving_device)).where(ReactionPlansHistory.help_message_id == help_message_id)
        plans_in_history = await self.__session.scalars(stmt)
        return [ReactionPlanHistoryGetModel.model_validate(plan) for plan in plans_in_history.all()]
