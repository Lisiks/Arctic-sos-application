from fastapi import APIRouter, status, Depends, Request, Path, Query
from fastapi.templating import Jinja2Templates
from typing import Annotated

from ..database.repositories import CrewsRepository, LifesavingDevicesRepository, HelpMessagesRepository, ReactPlansRepository, OperationActRepository, LieActRepository
from ..enums import Position, RescueAssetStatus, RescueAssetType, CommunicationChannelType, HelpMessageType, SourceType, WeatherCondition

templater = Jinja2Templates(directory="src/templates")

router = APIRouter(prefix="/site", tags=["<HTML>"])

@router.get("/crews", status_code=status.HTTP_200_OK)
async def crews(
    request: Request,
    repo: Annotated[CrewsRepository, Depends(CrewsRepository)]
):
    crews = await repo.get_all()
    return templater.TemplateResponse(
        name="crews.html",
        request=request,
        context={"crews": crews}
    )


@router.get("/crews/create", status_code=status.HTTP_200_OK)
async def create_crews(
    request: Request,
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)]
):
    livesaving_devises = await repo.get_all()
    positions = [position.value for position in Position]
    
    return templater.TemplateResponse(
        name="crews_create_form.html",
        request=request,
        context={"livesaving_devises": livesaving_devises, "positions": positions}
    )

@router.get("/crews/modify/{crew_id}", status_code=status.HTTP_200_OK)
async def update_crews(
    request: Request,
    crew_id: Annotated[int, Path(gt=0)],
    crews_repo:  Annotated[CrewsRepository, Depends(CrewsRepository)],
    lifesaving_devices_repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)]
):
    crew = await crews_repo.get_by_id(crew_id)

    if crew is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного сотрудника не существует!", "error_title": "Сотрудник не найден"}
        )

    livesaving_devises = await lifesaving_devices_repo.get_all()
    positions = [position.value for position in Position]


    return templater.TemplateResponse(
        name="crews_update_form.html",
        request=request,
        context={"livesaving_devises": livesaving_devises, "positions": positions, "crew": crew}
    )




@router.get("/lifesavingdevises", status_code=status.HTTP_200_OK)
async def lifesaving_devises(
    request: Request,
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)]
):
    lifesavind_devices = await repo.get_all()
    return templater.TemplateResponse(
        name="lifesaving_device.html",
        request=request,
        context={"lifesavind_devices": lifesavind_devices}
    )



@router.get("/lifesavingdevises/create", status_code=status.HTTP_200_OK)
async def lifesaving_devises_create(
    request: Request,
):  
    lifesaving_devises_types = [type_.value for type_ in RescueAssetType]
    lifesaving_devises_statuses = [status_.value for status_ in RescueAssetStatus]
    
    return templater.TemplateResponse(
        name="lifesaving_device_create_form.html",
        request=request,
        context={"lifesaving_devises_types": lifesaving_devises_types, "lifesaving_devises_statuses": lifesaving_devises_statuses}
    )



@router.get("/lifesavingdevises/modify/{device_id}", status_code=status.HTTP_200_OK)
async def lifesaving_devises_update(
    device_id: Annotated[int, Path(gt=0)],
    request: Request,
    repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)]
):
    device = await repo.get_by_id(device_id)

    if device is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - этого спасательного средства не существует!", "error_title": "Спасательное средство не найдено"}
        )

    lifesaving_devises_types = [type_.value for type_ in RescueAssetType]
    lifesaving_devises_statuses = [status_.value for status_ in RescueAssetStatus]


    return templater.TemplateResponse(
        name="lifesaving_device_update_form.html",
        request=request,
        context={"lifesaving_devises_types": lifesaving_devises_types, "lifesaving_devises_statuses": lifesaving_devises_statuses, "lifesaving_devise": device}
    )



@router.get("/messages", status_code=status.HTTP_200_OK)
async def messages(
    request: Request,
    repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    messages = await repo.get_all(page)
  
    return templater.TemplateResponse(
        name="messages.html",
        request=request,
        context={"messages": messages, "page": page}
    )


@router.get("/messages/create", status_code=status.HTTP_200_OK)
async def messages_create(
    request: Request,
):
    chanell_types = [chanell_type.value for chanell_type in CommunicationChannelType]
    incident_types = [incident_type.value for incident_type in HelpMessageType]
    sourse_types = [sourse_type.value for sourse_type in SourceType]
  
    return templater.TemplateResponse(
        name="message_create_form.html",
        request=request,
        context={"chanell_types": chanell_types, "incident_types": incident_types, "sourse_types": sourse_types}
    )


@router.get("/plans", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    plans = await repo.get_all(page)


    return templater.TemplateResponse(
        name="plan.html",
        request=request,
        context={"plans": plans, "page": page}
    )



@router.get("/plans/create/{message_id}", status_code=status.HTTP_200_OK)
async def plans_create(
    request: Request,
    lifesaving_davices_repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
    messages_repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    message_id: Annotated[int, Path(gt=0)]
):
    message = await messages_repo.get_by_id(message_id)

    if message is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного сообщения не существует!", "error_title": "Сообщение не найдено!"}
        )

    livesaving_devises = await lifesaving_davices_repo.get_all()
    weather_conditions = [condition.value for condition in WeatherCondition]
  
    return templater.TemplateResponse(
        name="plan_create_form.html",
        request=request,
        context={"livesaving_devises": livesaving_devises, "weather_conditions": weather_conditions, "message": message}
    )



@router.get("/plans/modify/{message_id}", status_code=status.HTTP_200_OK)
async def plans_update(
    request: Request,
    lifesaving_davices_repo: Annotated[LifesavingDevicesRepository, Depends(LifesavingDevicesRepository)],
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    message_id: Annotated[int, Path(gt=0)]
):
    plan = await repo.get_plan_by_id(message_id)

    if plan is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного плана не существует!", "error_title": "План не найден!"}
        )

    livesaving_devises = await lifesaving_davices_repo.get_all()
    weather_conditions = [condition.value for condition in WeatherCondition]
  
    return templater.TemplateResponse(
        name="plan_update_form.html",
        request=request,
        context={"livesaving_devises": livesaving_devises, "weather_conditions": weather_conditions, "plan": plan}
    )


@router.get("/plans/{message_id}/history", status_code=status.HTTP_200_OK)
async def plans_history(
    request: Request,
    repo: Annotated[ReactPlansRepository, Depends(ReactPlansRepository)],
    message_id: Annotated[int, Path(gt=0)]
):
    plan = await repo.get_plan_by_id(message_id)
    
    if plan is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного плана не существует!", "error_title": "План не найден!"}
        )

    history = await repo.get_history(message_id)

    return templater.TemplateResponse(
        name="plan_history.html",
        request=request,
        context={"plans": history, "main_plan": plan}
    )



@router.get("/act/create/{message_id}", status_code=status.HTTP_200_OK)
async def act_create(
    request: Request,
    messages_repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    message_id: Annotated[int, Path(gt=0)]
):
    message = await messages_repo.get_by_id(message_id)

    if message is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного сообщения не существует!", "error_title": "Сообщение не найдено!"}
        )
  
    return templater.TemplateResponse(
        name="act_create_form.html",
        request=request,
        context={"message": message}
    )



@router.get("/lieact/create/{message_id}", status_code=status.HTTP_200_OK)
async def lie_act_create(
    request: Request,
    messages_repo: Annotated[HelpMessagesRepository, Depends(HelpMessagesRepository)],
    message_id: Annotated[int, Path(gt=0)]
):
    message = await messages_repo.get_by_id(message_id)

    if message is None:
        return templater.TemplateResponse(
            name="error_page.html",
            request=request,
            context={"message": "404 - данного сообщения не существует!", "error_title": "Сообщение не найдено!"}
        )
  
    return templater.TemplateResponse(
        name="lie_act_create_form.html",
        request=request,
        context={"message": message}
    )




@router.get("/act", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    repo: Annotated[OperationActRepository, Depends(OperationActRepository)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    acts = await repo.get_all(page)

    return templater.TemplateResponse(
        name="act.html",
        request=request,
        context={"acts": acts, "page": page}
    )


@router.get("/lieact", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
    repo: Annotated[LieActRepository, Depends(LieActRepository)],
    page: Annotated[int, Query(gt=0)] = 1,
):
    lie_acts = await repo.get_all(page)

    return templater.TemplateResponse(
        name="lie_act.html",
        request=request,
        context={"lie_acts": lie_acts, "page": page}
    )


@router.get("/reports", status_code=status.HTTP_200_OK)
async def plans_get(
    request: Request,
  
):
    return templater.TemplateResponse(
        name="reports.html",
        request=request,
    )


