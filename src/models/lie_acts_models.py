from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

class LieActBaseModel(BaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]
    reason_description: Annotated[str, Field(alias="reasonDescription")]
    action_description: Annotated[str, Field(alias="actionDescription")]
    fact_datetime: Annotated[datetime, Field(alias="factDatetime")]

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
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
    