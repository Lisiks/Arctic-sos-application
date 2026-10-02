from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

from ..enums import Position
from .lifesaving_devises_models import LivesavingDeviceGetModel

class CrewBaseModel(BaseModel):
    f: Annotated[str, Field(max_length=100, min_length=2)]
    i: Annotated[str, Field(max_length=100, min_length=2)]
    o: Annotated[str, Field(max_length=100, min_length=2)]
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
    lifesaving_device: LivesavingDeviceGetModel

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )


