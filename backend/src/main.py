from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from passlib.context import CryptContext

from src.healthcare_api.api.patient_data import router as patient_data_router
from src.healthcare_api.api.auth import router as auth_router
from .settings import settings


def setup_app() -> FastAPI:
    app = FastAPI()  # noqa
    app.include_router(auth_router)
    app.include_router(patient_data_router)
    app.add_middleware(DBSessionMiddleware, db_url=settings.SQLALCHEMY_DATABASE_URI)
    app.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return app


app = setup_app()
