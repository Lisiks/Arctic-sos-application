from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Annotated, Optional
from datetime import datetime

from ..enums import SourceType


class SourceBaseModel(BaseModel):
    name: Annotated[str, Field(max_length=100, min_length=3)]
    latitude: Annotated[float, Field(ge=-180.0, le=180)]
    longitude: Annotated[float, Field(ge=-180.0, le=180)]
    source_type: Annotated[SourceType, Field(alias="sourceType")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )


class SourcePostModel(SourceBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )


class SourceGetModel(SourceBaseModel):
    id: int
    need_check: Annotated[bool, Field(alias="needCheck")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )