from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..enums import SourceType, HelpMessageType, CommunicationChannelType, IncidentStatus


class HelpMessageBaseModel(BaseModel):
    source_type: Annotated[SourceType, Field(alias="sourceType")]
    latitude: Annotated[float, Field(ge=-180.0, le=180)]
    longitude: Annotated[float, Field(ge=-180.0, le=180)]
    incident_type: Annotated[HelpMessageType, Field(alias="incidentType")]
    incident_description: Annotated[str, Field(alias="incidentDescription")]
    chanell_type: Annotated[CommunicationChannelType, Field(alias="chanellType")]
    datetime: datetime
    status: Annotated[Optional[IncidentStatus], Field(default=IncidentStatus.IN_PROGRESS)]

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

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )