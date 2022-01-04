from datetime import timedelta, datetime

from jose import JWTError, jwt  # noqa
from fastapi import Header, Depends
from passlib.context import CryptContext

from src.exceptions import NoUserInDbException, BadPasswordException, JWTException
from src.healthcare_api.models import User
from src.healthcare_api.schemas.user import UserSchema
from src.settings import settings


def get_auth_token(token: str = Header(..., alias="Authorization")) -> str:
    return token.split("Bearer")[-1].strip()


def verify_password(pwd_context: CryptContext, plain_password: str, db_password: str) -> bool:
    return pwd_context.verify(plain_password, db_password)


def get_user(username: str) -> UserSchema:
    user = User.get_user_by_username(username)
    if not user:
        raise NoUserInDbException(username)
    return user


def current_user(token: str = Depends(get_auth_token)) -> UserSchema:
    if settings.AUTHORIZATION_OFF:
        return UserSchema(id=0, username="no-auth-user", password="X"*12, active=True)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise NoUserInDbException("")
    except JWTError:
        raise JWTException
    user = get_user(username)
    if user is None:
        raise NoUserInDbException(username)
    return user


def check_credentials(pwd_context: CryptContext, username: str, password: str) -> UserSchema:
    user = get_user(username)
    if not user:
        raise NoUserInDbException(username)
    if not verify_password(pwd_context, password, user.password):
        raise BadPasswordException(username)
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
