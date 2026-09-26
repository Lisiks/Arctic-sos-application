from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


class OperationActBaseModel(BaseModel):
    help_message_id: Annotated[int, Field(alias="helpMessageId")]
    resque_count: Annotated[int, Field(ge=0, alias="resqueCount")]
    help_info: Annotated[str, Field("helpInfo")]
    resourses_info: Annotated[str, Field("resoursesInfo")]
    fact_datetime: Annotated[datetime, Field(alias="factDatetime")]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=False
    )


class OperationActPostModel(OperationActBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class OperationActGetModel(OperationActBaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        serialize_by_alias=True
    )
