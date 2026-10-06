from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional

from datetime import datetime

from ..enums import WeatherCondition
from .short_models import LifesavingDeviceShortMode
from .help_messages_models import HelpMessageGetModel
from .users_models import UserGetModel


class ReactionPlanBaseModel(BaseModel):
    lifesaving_devices_id: Annotated[int, Field(alias="lifesavingDevicesId")]
    planning_time: Annotated[datetime, Field(alias="planningDatetime")]
    weather_condition: Annotated[list[WeatherCondition], Field(alias="weatherCondition")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )

    @field_validator("planning_time", mode="after")
    @classmethod
    def replase_dt_timezone(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=None)

class ReactionPlanPostModel(ReactionPlanBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class ReactionPlanGetModel(ReactionPlanBaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]
    help_message: HelpMessageGetModel
    lifesaving_device: Annotated[LifesavingDeviceShortMode, Field(alias="lifesavingDevice")]

    user_id: Optional[int]
    user: Optional[UserGetModel]
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )

class ReactionPlanHistoryGetModel(ReactionPlanBaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]
    lifesaving_device: Annotated[LifesavingDeviceShortMode, Field(alias="lifesavingDevice")]
    change_datetime: Annotated[datetime, Field(alias="changeDatetime")]

    user_id: Optional[int]
    user: Optional[UserGetModel]
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
