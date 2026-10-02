from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional


from ..enums import RescueAssetStatus, RescueAssetType

class LivesavingDeviceBaseModel(BaseModel):
    type: RescueAssetType
    name: Annotated[str, Field(max_length=200, min_length=5)]
    latitude: Annotated[float, Field(ge=-180.0, le=180)]
    longitude: Annotated[float, Field(ge=-180.0, le=180)]
    reach_zone_km: Annotated[float, Field(gt=0, alias="reachZoneKm")]
    status: Annotated[Optional[RescueAssetStatus], Field(default=RescueAssetStatus.READY)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )


class LivesavingDevicePostModel(LivesavingDeviceBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )


class LivesavingDeviceGetModel(LivesavingDeviceBaseModel):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
