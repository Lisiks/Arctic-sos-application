from fastapi import Depends, APIRouter, status, Form, Path
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from typing import Annotated

from ..core import config
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel, UserJWTModel
from ..utils import auth
from ..services import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create(
    user_data: Annotated[UserPostModel, Form(media_type="application/x-www-form-urlencoded")],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    service: Annotated[UsersService, Depends(UsersService)]
) -> dict[str, str]:
    await service.create_user(user_data, auth_data)
    return {"msg": "created"}


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete(
    user_id: Annotated[int, Path(gt=0)],
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    service: Annotated[UsersService, Depends(UsersService)]
) -> dict[str, str]:
    await service.delete_user(user_id, auth_data)
    return {"msg": "deleted"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserGetModel])
async def get_all(
    auth_data: Annotated[UserJWTModel, Depends(auth)],
    service: Annotated[UsersService, Depends(UsersService)]
) -> list[UserGetModel]:
    return await service.get_all(auth_data)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: Annotated[UserLoginModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[UsersService, Depends(UsersService)]
):
    token = await service.login_user(login_data)
    responce = JSONResponse(content={"msg": "ok"})
    responce.set_cookie(
        key=config.jwt.cookie,
        value=token,
        samesite="lax",
        httponly=True
    )
    return responce


@router.post("/logout", status_code=status.HTTP_303_SEE_OTHER, response_model=dict[str, str])
async def logout() -> dict[str, str]:
    responce = RedirectResponse("/site/login", status_code=status.HTTP_303_SEE_OTHER)
    responce.delete_cookie(key=config.jwt.cookie)
    return responce