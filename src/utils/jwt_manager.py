from fastapi import Cookie

import jwt

from typing import Annotated, Optional
from datetime import datetime, timedelta

from ..core import config
from ..exceptions import DeletedUserException
from ..models.users_models import UserGetModel, UserJWTModel


class JWTManager:
    __deleted_user_id = set()

    @classmethod
    def create_jwt(cls, user_data: UserGetModel) -> str:
        payload = {
            "sub": user_data.model_dump_json(),
            "exp": datetime.now() + timedelta(seconds=config.jwt.expire)
        }
        return jwt.encode(payload, config.jwt.secret, algorithm="HS256")
    
    @classmethod
    def verify_jwt(cls, token: str) -> UserJWTModel:
        payload = jwt.decode(token, config.jwt.secret, algorithms=["HS256"])
        user_data = UserJWTModel.model_validate_json(payload["sub"])
        if user_data.id in cls.__deleted_user_id:
            raise DeletedUserException("This user was deleted!")

        return user_data

    @classmethod
    def add_deleted_user_id(cls, user_id: int) -> None:
        cls.__deleted_user_id.add(user_id)


def auth(
    token: Annotated[Optional[str], Cookie(alias=config.jwt.cookie)] = None
) -> UserJWTModel:
    return JWTManager.verify_jwt(token)
        

