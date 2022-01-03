from datetime import timedelta

from fastapi import APIRouter, Depends
from passlib.context import CryptContext

from ..models import User
from ..schemas.authentication import JWTSchema
from ..schemas.user import UserPostSchema, UserSchema
from ..utils.authentication import current_user, check_credentials, create_access_token
from ...deps import get_pwd_context
from ...settings import settings

router = APIRouter(tags=["Auth"])


@router.post("/register")
async def register(
    user_post_schema: UserPostSchema,
    pwd_context: CryptContext = Depends(get_pwd_context),
):
    pwd_hash = pwd_context.encrypt(user_post_schema.password)
    new_user = User.add(username=user_post_schema.username, password=pwd_hash)

    return new_user


@router.post("/authenticate")
async def authenticate(
    auth_body: UserPostSchema, pwd_context: CryptContext = Depends(get_pwd_context)
):
    user = check_credentials(pwd_context, auth_body.username, auth_body.password)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return JWTSchema(access_token=access_token)


@router.get("/users/me")
async def get_current_user(user: UserSchema = Depends(current_user)):
    return user
