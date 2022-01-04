from http import HTTPStatus

from fastapi.exceptions import HTTPException


# General exceptions
class CreateUserException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            detail={
                "status": "Bad request.",
                "title": "Cannot create user.",
                "detail": f"User with username '{username}' cannot be created.",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )


class CannotCreateObjectException(HTTPException):
    def __init__(self):
        super().__init__(
            detail={
                "status": "Bad request.",
                "title": "Cannot create object.",
                "detail": "Cannot create object.",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )


class ValidationErrorException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            detail={
                "status": "Bad request.",
                "title": "Cannot parse data.",
                "detail": message,
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )


# Authentication exceptions
class NoUserInDbException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            detail={
                "status": "Not found.",
                "title": "User not found.",
                "detail": f"User '{username}' not found.",
            },
            status_code=HTTPStatus.NOT_FOUND,
        )


class BadPasswordException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            detail={
                "status": "Forbidden.",
                "title": "Bad password.",
                "detail": f"Bad password for user '{username}'",
            },
            status_code=HTTPStatus.FORBIDDEN,
        )


class JWTException(HTTPException):
    def __init__(self):
        super().__init__(
            detail={
                "status": "Bad request.",
                "title": "JWT Error.",
                "detail": "Cannot decode JWT",
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
