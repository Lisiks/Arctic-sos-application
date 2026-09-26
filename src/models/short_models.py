from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

from ..enums import RescueAssetType, RescueAssetStatus

class LifesavingDeviceShortMode(BaseModel):
    id: int
    type: RescueAssetType
    status: Annotated[Optional[RescueAssetStatus], Field(default=RescueAssetStatus.READY)]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore"
    )