from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, extract, case
from fastapi import Depends
from typing import Annotated

from ...core.database import get_session

from ..shemas import LieActs, OperationActs, HelpMessages, ReactionPlans, LifesavingDevices
from ...enums.lifesaving_devices_enums import RescueAssetStatus

class ReportsRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.__session = session

    async def message_per_type_report(self) -> tuple:
        stmt = select(
            HelpMessages.incident_type, 
            func.count(HelpMessages.id).label("message count")
        ).group_by(HelpMessages.incident_type).order_by(HelpMessages.incident_type)
        result =  await self.__session.execute(stmt)
        return result.all()


    async def avg_reaction_time_report(self) -> tuple:
        ops_avg = (
            select(
                func.avg(func.extract("epoch",OperationActs.fact_datetime - HelpMessages.datetime)).label("avg_seconds")
            ).join(
                HelpMessages, HelpMessages.id == OperationActs.help_message_id
            ).scalar_subquery()
        )

   
        lie_avg = (
            select(
                func.avg(func.extract("epoch",LieActs.fact_datetime - HelpMessages.datetime)).label("avg_seconds")
            ).join(
                HelpMessages, HelpMessages.id == LieActs.help_message_id
            ).scalar_subquery()
        )

        stmt = select(
            ((ops_avg + lie_avg) / 2.0).label("avg_between_seconds"),
        )

        result =  await self.__session.execute(stmt)
        return result.all()

        

    async def lie_acts_count_report(self) -> tuple:
        ops_act_count = select(
            func.count(OperationActs.help_message_id).label("operation_count")
        ).scalar_subquery()

        lie_act_count = select(
            func.count(LieActs.help_message_id).label("lie_act_count")
        ).scalar_subquery()

        stmt = select(
            ops_act_count,
            lie_act_count,
            ((lie_act_count) / (ops_act_count + lie_act_count))
        )
        
        result = await self.__session.execute(stmt)
        return result.all()

    async def lefesaving_device_ready_count_report(self) -> tuple:
        stmt = select(
            LifesavingDevices.type,
            func.count(LifesavingDevices.id).label("device_count")
        ).where(
            LifesavingDevices.status == RescueAssetStatus.READY
        ).group_by(LifesavingDevices.type).order_by(LifesavingDevices.type)

        result = await self.__session.execute(stmt)
        return result.all()


    async def messages_per_seasons_report(self) -> tuple:
        month = extract("month", HelpMessages.datetime)

        season = case(
            (month.in_([12, 1, 2]), "зима"),
            (month.in_([3, 4, 5]),  "весна"),
            (month.in_([6, 7, 8]),  "лето"),
            else_="осень",
        ).label("season")

        stmt = (
            select(season, func.count().label("cnt"))
            .group_by(season)
            .order_by(
                case(
                    (season == "зима", 1),
                    (season == "весна", 2),
                    (season == "лето", 3),
                    else_=4,
                )
            )
        )

        result = await self.__session.execute(stmt)
        return result.all()