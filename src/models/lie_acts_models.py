from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from datetime import datetime


class LieActBaseModel(BaseModel):
    reason_description: Annotated[str, Field(alias="reasonDescription")]
    action_description: Annotated[str, Field(alias="actionDescription")]
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


class LieActPostModel(LieActBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class LieActGetModel(LieActBaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
    