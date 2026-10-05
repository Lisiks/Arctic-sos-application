from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError, DBAPIError

from .settings import config
from ..exceptions import DeleteSuperuserException, DeletedUserException, FailedLoginException, IncorrectUserRole, NotFoundRecordException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def set_exc_handlers(app: FastAPI):
    @app.exception_handler(ExpiredSignatureError)
    def expired_token_error(request: Request, exc: ExpiredSignatureError):
        responce = RedirectResponse("/site/login", status_code=status.HTTP_303_SEE_OTHER)
        responce.delete_cookie(key=config.jwt.cookie)
        return responce


    @app.exception_handler(InvalidTokenError)
    def invalid_token_error(request: Request, exc: InvalidTokenError):
        responce = RedirectResponse("/site/login", status_code=status.HTTP_303_SEE_OTHER)
        responce.delete_cookie(key=config.jwt.cookie)
        return responce

    @app.exception_handler(DeleteSuperuserException)
    def deleted_superuser_error(request: Request, exc: DeleteSuperuserException):
        return JSONResponse(content={"msg": "you cannot delete superuser"}, status_code=status.HTTP_401_UNAUTHORIZED)

    @app.exception_handler(DeletedUserException)
    def deleted_user_error(request: Request, exc: DeletedUserException):
        return JSONResponse(content={"msg": "user was deleted"}, status_code=status.HTTP_403_FORBIDDEN)

    @app.exception_handler(IncorrectUserRole)
    def incorrect_user_role_exception(request: Request, exc: IncorrectUserRole):
        return RedirectResponse("/site/403", status_code=status.HTTP_303_SEE_OTHER)

    @app.exception_handler(NotFoundRecordException)
    def no_found_record_exception_handler(request: Request, exc: NotFoundRecordException):
        return RedirectResponse("/site/404", status_code=status.HTTP_303_SEE_OTHER)

    @app.exception_handler(FailedLoginException)
    def failed_login_exception(request: Request, exc: FailedLoginException):
        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_401_UNAUTHORIZED)
    

    @app.exception_handler(IntegrityError)
    def integrity_error_exc_handler(request: Request, exc: IntegrityError):
        exc_description = exc.args[0]

        if "insert or update on table \"crews\" violates foreign key constraint \"lifesaving_device_fk\"" in exc_description:
            return JSONResponse(content={"msg": "This lifesabing device doesnt exists!"}, status_code=status.HTTP_400_BAD_REQUEST)
        
        elif "update or delete on table \"lifesaving_devices\" violates foreign key constraint \"lifesaving_device_fk\" on table \"reaction_plans\"" in exc_description:
            return JSONResponse(content={"msg": "Cannot delete this lifesavind device, because it used in reaction plans!"}, status_code=status.HTTP_409_CONFLICT)
        
        elif "update or delete on table \"lifesaving_devices\" violates foreign key constraint \"lifesaving_device_fk\" on table \"crews\"" in exc_description:
            return JSONResponse(content={"msg": "Cannot delete this lifesavind device, because it has crews!"}, status_code=status.HTTP_409_CONFLICT)

        elif "duplicate key value violates unique constraint \"reaction_plans_pkey\"" in exc_description:
            return JSONResponse(content={"msg": "For this message already exists plan!"}, status_code=status.HTTP_409_CONFLICT)

        elif "insert or update on table \"reaction_plans\" violates foreign key constraint \"help_message_fk\"" in exc_description:
            return JSONResponse(content={"msg": "This help message doesnt exists!"}, status_code=status.HTTP_409_CONFLICT)

        elif "insert or update on table \"reaction_plans\" violates foreign key constraint \"lifesaving_device_fk\"" in exc_description:
            return JSONResponse(content={"msg": "This lifesaving device doesnt exists!"}, status_code=status.HTTP_409_CONFLICT)



        elif "insert or update on table \"operation_acts\" violates foreign key constraint \"help_message_fk\"" in exc_description:
            return JSONResponse(content={"msg": "This message doesnt exists!"}, status_code=status.HTTP_409_CONFLICT)

        elif "duplicate key value violates unique constraint \"operation_acts_pkey\"" in exc_description:
            return JSONResponse(content={"msg": "For this message already exists operation act!"}, status_code=status.HTTP_409_CONFLICT)



        elif "insert or update on table \"lie_acts\" violates foreign key constraint \"help_message_fk\"" in exc_description:
            return JSONResponse(content={"msg": "This message doesnt exists!"}, status_code=status.HTTP_409_CONFLICT)

        elif "duplicate key value violates unique constraint \"lie_acts_pkey\"" in exc_description:
            return JSONResponse(content={"msg": "For this message already exists lie act!"}, status_code=status.HTTP_409_CONFLICT)

        elif "uplicate key value violates unique constraint \"users_username_key\"" in exc_description:
            return JSONResponse(content={"msg": "User with this username already exists in database!"}, status_code=status.HTTP_409_CONFLICT)
        
        return JSONResponse(content={"msg": "server_db_error"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @app.exception_handler(DBAPIError)
    def dbapi_exc_handler(request: Request, exc: DBAPIError):
        exc_description = exc.args[0]
        if "Lifesaving devices cannot be used for this operation, because it has small reach zone for this operation" in exc_description:
            return JSONResponse(content={"msg": "Lifesaving devices cannot be used for this operation, because it has small reach zone for this operation!"}, status_code=status.HTTP_409_CONFLICT)

        elif "Lifesaving devices cannot be used for this operation, because its status is" in exc_description:
            return JSONResponse(content={"msg": "Lifesaving devices doesnt ready!"}, status_code=status.HTTP_409_CONFLICT)

        elif "This help message already done" in exc_description:
            return JSONResponse(content={"msg": "This help message already done!"}, status_code=status.HTTP_409_CONFLICT)

        elif "Lifesaving devices cannot be used for this operation, because its type is helicopter and we have bad weather in reaction plan information" in exc_description:
            return JSONResponse(content={"msg": "Bad weather for helecopter!"}, status_code=status.HTTP_409_CONFLICT)

        elif "Planning time smaller than help call time" in exc_description:
            return JSONResponse(content={"msg": "Planning time smaller, than message call time!"}, status_code=status.HTTP_409_CONFLICT)




        elif "Operation fact time smaller than call time" in exc_description:
            return JSONResponse(content={"msg": "Fact operation time smaller, than message call time!"}, status_code=status.HTTP_409_CONFLICT)

        elif "On this help message already exists act for lie call" in exc_description:
            return JSONResponse(content={"msg": "On this help message already exists act for lie call!"}, status_code=status.HTTP_409_CONFLICT)



        elif "On this help message already exists opeartion act" in exc_description:
             return JSONResponse(content={"msg": "On this help message already exists operation act!"}, status_code=status.HTTP_409_CONFLICT)

        return JSONResponse(content={"msg": "server_db_error"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)