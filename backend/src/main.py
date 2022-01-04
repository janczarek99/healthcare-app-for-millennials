from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from passlib.context import CryptContext

from src.healthcare_api.api.patient_data import router as patient_data_router
from src.healthcare_api.api.auth import router as auth_router
from src.healthcare_api.api.documents import router as documents_router
from .healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from .healthcare_api.utils.azure_ocr_client import AzureOCRClient
from .settings import settings


def setup_app() -> FastAPI:
    app = FastAPI()  # noqa
    app.include_router(auth_router)
    app.include_router(patient_data_router)
    app.include_router(documents_router)
    app.add_middleware(DBSessionMiddleware, db_url=settings.SQLALCHEMY_DATABASE_URI)
    app.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    app.azure_storage_client = AzureBlobStorageClient()
    app.azure_ocr_client = AzureOCRClient()
    return app


app = setup_app()
