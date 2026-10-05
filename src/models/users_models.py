from pydantic import BaseModel, Field, ConfigDict, computed_field
from typing import Annotated, Optional

from ..enums import UserRoles


class UserBaseModel(BaseModel):
    username: Annotated[str, Field(max_length=30, min_length=6)]
    role: UserRoles

    model_config = ConfigDict(
        from_attributes=True
    )

class UserLoginModel(BaseModel):
    username: Annotated[str, Field(max_length=30, min_length=6)]
    plain_password: Annotated[str, Field(max_length=72, min_length=6, alias="plainPassword", exclude=True)]

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )


class UserPostModel(UserBaseModel):
    plain_password: Annotated[str, Field(max_length=72, min_length=6, alias="plainPassword", exclude=True)]
    password_hash: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        serialize_by_alias=False
    )

class UserGetModel(UserBaseModel):
    id: int
    password_hash: Annotated[str, Field(exclude=True)]

class UserJWTModel(UserBaseModel):
    id: int

    

