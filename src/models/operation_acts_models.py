from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from datetime import datetime

from .help_messages_models import HelpMessageGetModel
from .users_models import UserGetModel


class OperationActBaseModel(BaseModel):
    resque_count: Annotated[int, Field(ge=0, alias="resqueCount")]
    help_info: Annotated[str, Field(alias="helpInfo")]
    resourses_info: Annotated[str, Field(alias="resoursesInfo")]
    fact_datetime: Annotated[datetime, Field(alias="factDatetime")]

    @field_validator("fact_datetime", mode="after")
    @classmethod
    def replase_dt_timezone(cls, value: datetime) -> datetime:
            return value.replace(tzinfo=None)

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )


class OperationActPostModel(OperationActBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class OperationActGetModel(OperationActBaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]
    help_message: HelpMessageGetModel

    user_id: Optional[int]
    user: Optional[UserGetModel]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
