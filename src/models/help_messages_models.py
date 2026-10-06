from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from datetime import datetime

from ..enums import HelpMessageType, CommunicationChannelType, IncidentStatus
from .sources_models import SourceGetModel


class HelpMessageBaseModel(BaseModel):
    sourse_id: Annotated[int, Field(gt=0, alias="sourceId")]
    incident_type: Annotated[HelpMessageType, Field(alias="incidentType")]
    incident_description: Annotated[str, Field(alias="incidentDescription")]
    chanell_type: Annotated[CommunicationChannelType, Field(alias="chanellType")]
    datetime: datetime

    @field_validator("datetime", mode="after")
    @classmethod
    def replase_dt_timezone(cls, value: datetime) -> datetime:
        return value.replace(tzinfo=None)

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )

class HelpMessagePostModel(HelpMessageBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class HelpMessageGetModel(HelpMessageBaseModel):
    id: int
    source: SourceGetModel
    status: IncidentStatus

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )