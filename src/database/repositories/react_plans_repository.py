from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, desc
from fastapi import Depends
from typing import Annotated
from datetime import datetime

from ...core.database import get_session
from ...models.reaction_plans_models import ReactionPlanGetModel, ReactionPlanPostModel, ReactionPlanHistoryGetModel
from ..shemas import ReactionPlans, ReactionPlansHistory, HelpMessages


class ReactPlansRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session


    async def create(self, message_id: int, plan_params: ReactionPlanPostModel, user_id: int) -> None:
        plan = ReactionPlans(**plan_params.model_dump(), help_message_id=message_id, user_id=user_id)
        self.__session.add(plan)
        await self.__session.flush()

        plan_histoty = ReactionPlansHistory(
            **plan_params.model_dump(),
            change_datetime = datetime.now(),
            help_message_id = message_id,
            user_id=user_id
        )
        self.__session.add(plan_histoty)

        await self.__session.commit()


    async def modify(self, message_id: int, plan_params: ReactionPlanPostModel, user_id: int) -> None:
        plan = await self.__session.get(ReactionPlans, message_id)

        if plan is not None:
            for field, value in plan_params.model_dump().items():
                setattr(plan, field, value)
            plan.user_id = user_id
            await self.__session.flush()

            plan_histoty = ReactionPlansHistory(
                **plan_params.model_dump(),
                change_datetime = datetime.now(),
                help_message_id = message_id,
                user_id=user_id
            )
            self.__session.add(plan_histoty)
    
            await self.__session.commit()


    async def get_all(self, page: int) -> list[ReactionPlanGetModel]:
        stmt = select(ReactionPlans).options(
            joinedload(ReactionPlans.lifesaving_device), 
            joinedload(ReactionPlans.help_message).joinedload(HelpMessages.source),
            joinedload(ReactionPlans.user)
        ).order_by(desc(ReactionPlans.planning_time), ReactionPlans.help_message_id).limit(30).offset((page - 1) * 30)
        plans = await self.__session.scalars(stmt)
        return [ReactionPlanGetModel.model_validate(plan) for plan in plans.all()]

    async def get_plan_by_id(self, message_id) -> ReactionPlanGetModel | None:
        stmt = select(ReactionPlans).options(
            joinedload(ReactionPlans.lifesaving_device), 
            joinedload(ReactionPlans.help_message).joinedload(HelpMessages.source),
            joinedload(ReactionPlans.user)
        ).where(ReactionPlans.help_message_id == message_id)
        plan = await self.__session.scalar(stmt)
        return ReactionPlanGetModel.model_validate(plan) if plan is not None else None


    async def get_history(self, message_id: int) -> list[ReactionPlanHistoryGetModel]:
        stmt = select(ReactionPlansHistory).options(joinedload(ReactionPlansHistory.lifesaving_device), joinedload(ReactionPlansHistory.user)).where(ReactionPlansHistory.help_message_id == message_id).order_by(desc(ReactionPlansHistory.change_datetime))
        plans_in_history = await self.__session.scalars(stmt)
        return [ReactionPlanHistoryGetModel.model_validate(plan) for plan in plans_in_history.all()]
