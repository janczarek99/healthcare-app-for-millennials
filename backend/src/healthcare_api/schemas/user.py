from pydantic import BaseModel, validator

from src.exceptions import ValidationErrorException


class UserPostSchema(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, v: str) -> str:
        if len(v) < 6:
            raise ValidationErrorException("Username length must be greater than or equal to 6.")
        return v

    @validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 10:
            raise ValidationErrorException("Password length must be greater than or equal to 10.")
        return v


class UserSchema(UserPostSchema):
    class Config:
        orm_mode = True

    id: int
    active: bool
