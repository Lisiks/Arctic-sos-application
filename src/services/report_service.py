from fastapi import Depends
from typing import Annotated
from io import BytesIO
import asyncio

from ..enums import UserRoles
from ..models.users_models import UserJWTModel
from ..database.repositories import ReportsRepository
from ..utils import ExcelBuferManager
from ..exceptions import IncorrectUserRole


class RepotsService:
    def __init__(self, repository: Annotated[ReportsRepository, Depends(ReportsRepository)]):
        self.__repository = repository


    async def create_message_per_type_report(self, auth_data: UserJWTModel) -> BytesIO:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        report_data = await self.__repository.message_per_type_report()
        buffer = await asyncio.to_thread(ExcelBuferManager.make_message_per_type_report, report_data)

        return buffer


    async def create_creaction_avg_report(self, auth_data: UserJWTModel) -> BytesIO:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        report_data = await self.__repository.avg_reaction_time_report()
        buffer = await asyncio.to_thread(ExcelBuferManager.make_avg_reaction_time_report, report_data)

        return buffer


    async def create_lie_acts_percent_report(self, auth_data: UserJWTModel) -> BytesIO:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        report_data = await self.__repository.lie_acts_count_report()
        buffer = await asyncio.to_thread(ExcelBuferManager.make_acts_count_report, report_data)

        return buffer


    async def create_lifesaving_devices_ready_count_report(self, auth_data: UserJWTModel) -> BytesIO:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")
        
        report_data = await self.__repository.lefesaving_device_ready_count_report()
        buffer = await asyncio.to_thread(ExcelBuferManager.make_devices_ready_count_report, report_data)

        return buffer


    async def create_message_per_season_report(self, auth_data: UserJWTModel) -> BytesIO:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")
        
        report_data = await self.__repository.messages_per_seasons_report()
        buffer = await asyncio.to_thread(ExcelBuferManager.make_message_per_seasons_report, report_data)

        return buffer