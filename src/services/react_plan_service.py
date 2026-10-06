from fastapi import Depends
from typing import Annotated

from ..models.reaction_plans_models import ReactionPlanGetModel, ReactionPlanPostModel, ReactionPlanHistoryGetModel
from ..models.users_models import UserJWTModel
from ..database.repositories import ReactPlansRepository
from ..enums import Position, UserRoles
from ..exceptions import IncorrectUserRole, NotFoundRecordException


class ReactionPlanService:
    def __init__(self, repository: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)]):
        self.__repository = repository


    async def create(self, message_id: int, plan_params: ReactionPlanPostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.create(message_id, plan_params, auth_data.id)


    async def modify(self, message_id: int, plan_params: ReactionPlanPostModel, auth_data: UserJWTModel) -> None:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER}:
            raise IncorrectUserRole("This function only for superuser and administrator!")

        await self.__repository.modify(message_id, plan_params, auth_data.id)


    async def get_by_id(self, message_id, auth_data: UserJWTModel) -> ReactionPlanGetModel:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        plan = await self.__repository.get_plan_by_id(message_id)

        if plan is None:
            raise NotFoundRecordException("Message doesn't found!")

        return plan

    async def get_all(self, page: int, auth_data: UserJWTModel) -> list[ReactionPlanGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_all(page)


    async def get_history(self, message_id: int, auth_data: UserJWTModel) -> list[ReactionPlanHistoryGetModel]:
        if auth_data.role not in {UserRoles.ADMIN, UserRoles.SUPERUSER, UserRoles.ANNALYTIC}:
            raise IncorrectUserRole("This function only for superuser, administrator and analythic!")

        return await self.__repository.get_history(message_id)