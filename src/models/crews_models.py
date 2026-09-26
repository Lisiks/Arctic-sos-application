from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

from ..enums import Position, RescueAssetType, RescueAssetStatus
from .short_models import LifesavingDeviceShortMode

class CrewBaseModel(BaseModel):
    f: Annotated[str, Field(max_length=100)]
    i: Annotated[str, Field(max_length=100)]
    o: Annotated[str, Field(max_length=100)]
    position: Position
    lifesaving_devices_id: Annotated[int, Field(alias="lifesavingDevicesId")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )


class CrewPostModel(CrewBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class CrewGetModel(CrewBaseModel):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )


class CrewGetModelWithLifesevingDevice(CrewGetModel):
    lifesaving_device: Annotated[LifesavingDeviceShortMode, Field(alias="lifesavingDevice")]