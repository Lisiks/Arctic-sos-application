from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from ..enums import RescueAssetType, RescueAssetStatus, SourceType, HelpMessageType, CommunicationChannelType, IncidentStatus

class LifesavingDeviceShortMode(BaseModel):
    id: int
    type: RescueAssetType
    status: Annotated[Optional[RescueAssetStatus], Field(default=RescueAssetStatus.READY)]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )

class HelpMessageShortModel(BaseModel):
    id: int
    source_type: Annotated[SourceType, Field(alias="sourceType")]
    incident_type: Annotated[HelpMessageType, Field(alias="incidentType")]
    datetime: datetime
    status: Annotated[Optional[IncidentStatus], Field(default=IncidentStatus.IN_PROGRESS)]

    model_config = ConfigDict(
        from_attributes=True,
        serialize_by_alias=True,
        validate_by_alias=False,
        extra="ignore"
    )