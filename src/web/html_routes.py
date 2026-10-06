from fastapi import APIRouter, status, Depends, Request, Path, Query
from fastapi.templating import Jinja2Templates
from typing import Annotated

from ..database.repositories import CrewsRepository, LifesavingDevicesRepository, HelpMessagesRepository, ReactPlansRepository, OperationActRepository, LieActRepository
from ..enums import Position, RescueAssetStatus, RescueAssetType, CommunicationChannelType, HelpMessageType, SourceType, WeatherCondition, UserRoles

from ..services import *
from ..utils.jwt_manager import auth
from ..models.users_models import UserJWTModel
from ..exceptions import IncorrectUserRole

templater = Jinja2Templates(directory="src/templates")

router = APIRouter(prefix="/site", tags=["<HTML>"])


@router.get("/403", status_code=status.HTTP_200_OK)
def error_403_page(
    request: Request, 
    auth_data: Annotated[UserJWTModel, Depends(auth)]
):
    return templater.TemplateResponse(
        name="error_page.html",
        request=request,
        context={"message": "403 - отказано в доступе", "error_title": "Вам не хватает прав для осущестлвения данных действий!", "user_data": auth_data}
    )


@router.get("/404", status_code=status.HTTP_200_OK)
def error_404_page(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    return templater.TemplateResponse(
        name="error_page.html",
        request=request,
        context={"message": "404 - не найдено", "error_title": "Измениемый/просматриваемый/удаляемый ресурс не найден!", "user_data": auth_data}
    )


@router.get("/crews", status_code=status.HTTP_200_OK)
async def crews(
    request: Request,
    service: Annotated[CrewsService, Depends(CrewsService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    crews = await service.get_all(auth_data)
    return templater.TemplateResponse(
        name="crews.html",
        request=request,
        context={"crews": crews, "user_data": auth_data}
    )


@router.get("/crews/create", status_code=status.HTTP_200_OK)
async def create_crews(
    request: Request,
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    livesaving_devises = await service.get_all(auth_data)
    
    return templater.TemplateResponse(
        name="crews_create_form.html",
        request=request,
        context={
            "livesaving_devises": livesaving_devises, 
            "positions": [position.value for position in Position],
            "user_data": auth_data
        }
    )

@router.get("/crews/modify/{crew_id}", status_code=status.HTTP_200_OK)
async def update_crews(
    request: Request,
    crew_id: Annotated[int, Path(gt=0)],
    crews_service:  Annotated[CrewsService, Depends(CrewsService)],

    device_service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    crew = await crews_service.get_by_id(crew_id, auth_data)
    livesaving_devises = await device_service.get_all(auth_data)

    return templater.TemplateResponse(
        name="crews_update_form.html",
        request=request,
        context={
            "livesaving_devises": livesaving_devises, 
            "positions": [position.value for position in Position], 
            "crew": crew,
            "user_data": auth_data
        }
    )




@router.get("/lifesavingdevises", status_code=status.HTTP_200_OK)
async def lifesaving_devises(
    request: Request,
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    lifesavind_devices = await service.get_all(auth_data)
    return templater.TemplateResponse(
        name="lifesaving_device.html",
        request=request,
        context={
            "lifesavind_devices": lifesavind_devices,
            "user_data": auth_data
        }
    )



@router.get("/lifesavingdevises/create", status_code=status.HTTP_200_OK)
async def lifesaving_devises_create(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)],
): 
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    return templater.TemplateResponse(
        name="lifesaving_device_create_form.html",
        request=request,
        context={
            "lifesaving_devises_types": [type_.value for type_ in RescueAssetType], 
            "lifesaving_devises_statuses": [status_.value for status_ in RescueAssetStatus],
            "user_data": auth_data
        }
    )


@router.get("/lifesavingdevises/modify/{device_id}", status_code=status.HTTP_200_OK)
async def lifesaving_devises_update(
    device_id: Annotated[int, Path(gt=0)],
    request: Request,
    service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    device = await service.get_by_id(device_id, auth_data)


    return templater.TemplateResponse(
        name="lifesaving_device_update_form.html",
        request=request,
        context={
            "lifesaving_devises_types": [type_.value for type_ in RescueAssetType], 
            "lifesaving_devises_statuses": [status_.value for status_ in RescueAssetStatus], 
            "lifesaving_devise": device,
            "user_data": auth_data
        }
    )


@router.get("/sources", status_code=status.HTTP_200_OK)
async def sources_get(
    request: Request,
    service: Annotated[SourcesService, Depends(SourcesService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    sources = await service.get_all(auth_data)
    return templater.TemplateResponse(
        name="sources.html",
        request=request,
        context={
            "sources": sources,
            "user_data": auth_data
        }
    )


@router.get("/sources/create", status_code=status.HTTP_200_OK)
async def sources_create(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)], 
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
  
    return templater.TemplateResponse(
        name="sources_create_form.html",
        request=request,
        context={
            "sourse_types": [sourse_type.value for sourse_type in SourceType],
            "user_data": auth_data
        }
    )


@router.get("/sources/modify/{source_id}", status_code=status.HTTP_200_OK)
async def sources_modify(
    request: Request,
    source_id: Annotated[int, Path(gt=0)],
    service: Annotated[SourcesService, Depends(SourcesService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)], 
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")

    source = await service.get_by_id(source_id, auth_data)
    
    return templater.TemplateResponse(
        name="sources_update_form.html",
        request=request,
        context={
            "sourse_types": [sourse_type.value for sourse_type in SourceType],
            "user_data": auth_data,
            "source": source
        }
    )


@router.get("/messages", status_code=status.HTTP_200_OK)
async def sources_get(
    request: Request,
    service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    messages = await service.get_all(page, auth_data)
    return templater.TemplateResponse(
        name="messages.html",
        request=request,
        context={
            "messages": messages,
            "user_data": auth_data,
            "page": page
        }
    )



@router.get("/messages/create", status_code=status.HTTP_200_OK)
async def messages_create(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    service: Annotated[SourcesService, Depends(SourcesService)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")

    sources = await service.get_all(auth_data)
  
    return templater.TemplateResponse(
        name="message_create_form.html",
        request=request,
        context={
            "chanell_types": [chanell_type.value for chanell_type in CommunicationChannelType], 
            "incident_types": [incident_type.value for incident_type in HelpMessageType], 
            "sources": sources,
            "user_data": auth_data
        }
    )


@router.get("/plans", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    plans = await service.get_all(page, auth_data)

    return templater.TemplateResponse(
        name="plan.html",
        request=request,
        context={
            "plans": plans, 
            "page": page,
            "user_data": auth_data
        }
    )



@router.get("/plans/create/{message_id}", status_code=status.HTTP_200_OK)
async def plans_create(
    request: Request,
    message_service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    device_service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    message_id: Annotated[int, Path(gt=0)]
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    message = await message_service.get_by_id(message_id, auth_data)
    livesaving_devises = await device_service.get_all(auth_data)
  
    return templater.TemplateResponse(
        name="plan_create_form.html",
        request=request,
        context={
            "livesaving_devises": livesaving_devises, 
            "weather_conditions": [condition.value for condition in WeatherCondition], 
            "message": message,
            "user_data": auth_data
        }
    )



@router.get("/plans/modify/{message_id}", status_code=status.HTTP_200_OK)
async def plans_update(
    request: Request,
    plans_service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    device_service: Annotated[LifesavingDeviceService, Depends(LifesavingDeviceService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    message_id: Annotated[int, Path(gt=0)]
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    plan = await plans_service.get_by_id(message_id, auth_data)
    livesaving_devises = await device_service.get_all(auth_data)
  
    return templater.TemplateResponse(
        name="plan_update_form.html",
        request=request,
        context={
            "livesaving_devises": livesaving_devises, 
            "weather_conditions": [condition.value for condition in WeatherCondition], 
            "plan": plan,
            "user_data": auth_data
        }
    )


@router.get("/plans/{message_id}/history", status_code=status.HTTP_200_OK)
async def plans_history(
    request: Request,
    plans_service: Annotated[ReactionPlanService, Depends(ReactionPlanService)],
    message_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    plan = await plans_service.get_by_id(message_id, auth_data)
    history = await plans_service.get_history(message_id, auth_data)

    return templater.TemplateResponse(
        name="plan_history.html",
        request=request,
        context={
            "plans": history, 
            "main_plan": plan,
            "user_data": auth_data
        }
    )



@router.get("/act/create/{message_id}", status_code=status.HTTP_200_OK)
async def act_create(
    request: Request,
    service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    message_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    message = await service.get_by_id(message_id, auth_data)

    return templater.TemplateResponse(
        name="act_create_form.html",
        request=request,
        context={
            "message": message,
            "user_data": auth_data
        }
    )



@router.get("/lieact/create/{message_id}", status_code=status.HTTP_200_OK)
async def lie_act_create(
    request: Request,
    service: Annotated[HelpMessageService, Depends(HelpMessageService)],
    message_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.ADMIN and auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser and administrator!")
    
    message = await service.get_by_id(message_id, auth_data)
  
    return templater.TemplateResponse(
        name="lie_act_create_form.html",
        request=request,
        context={
            "message": message,
            "user_data": auth_data
        }
    )




@router.get("/act", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    service: Annotated[OpeartionActService, Depends(OpeartionActService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    acts = await service.get_all(page, auth_data)

    return templater.TemplateResponse(
        name="act.html",
        request=request,
        context={
            "acts": acts, 
            "page": page,
            "user_data": auth_data
        }
    )


@router.get("/lieact", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    service: Annotated[LieActService, Depends(LieActService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    lie_acts = await service.get_all(page, auth_data)

    return templater.TemplateResponse(
        name="lie_act.html",
        request=request,
        context={
            "lie_acts": lie_acts, 
            "page": page,
            "user_data": auth_data
        }
    )



@router.get("/users", status_code=status.HTTP_200_OK)
async def users(
    request: Request,
    service: Annotated[UsersService, Depends(UsersService)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser!")
    
    users_ = await service.get_all(auth_data)
    return templater.TemplateResponse(
        name="users.html",
        request=request,
        context={
            "users": users_, 
            "user_data": auth_data
        }
    )


@router.get("/users/create", status_code=status.HTTP_200_OK)
async def users_create(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)],
):
    if auth_data.role != UserRoles.SUPERUSER:
        raise IncorrectUserRole("This function only for superuser!")
    
    return templater.TemplateResponse(
        name="users_create_form.html",
        request=request,
        context={
            "roles": [role.value for role in UserRoles if role != UserRoles.SUPERUSER], 
            "user_data": auth_data
        }
    )


@router.get("/reports", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    auth_data: Annotated[UserJWTModel, Depends(auth)],
  
):

    return templater.TemplateResponse(
        name="reports.html",
        request=request,
        context={
            "user_data": auth_data
        }
    )



@router.get("/login", status_code=status.HTTP_200_OK)
async def login_form(
    request: Request,
):
    return templater.TemplateResponse(
        name="login.html",
        request=request,
    )

