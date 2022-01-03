from pydantic import BaseModel, Field

from src.settings import settings


class JWTSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True

    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType", default="Bearer")
    expire_time_in_seconds: int = Field(
        alias="expireTimeInSeconds", default=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
