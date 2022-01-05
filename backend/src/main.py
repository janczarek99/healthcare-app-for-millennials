from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from passlib.context import CryptContext

from src.healthcare_api.api.auth import router as auth_router
from src.healthcare_api.api.documents import router as documents_router
from src.healthcare_api.api.photos import router as photos_router
from src.healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from src.healthcare_api.utils.azure_custom_vision_client import AzureCustomVisionClient
from src.healthcare_api.utils.azure_ocr_client import AzureOCRClient
from src.settings import settings


def setup_app() -> FastAPI:
    # Main app
    app = FastAPI()  # noqa

    # Views
    app.include_router(auth_router)
    app.include_router(documents_router)
    app.include_router(photos_router)

    # Middlewares
    app.add_middleware(DBSessionMiddleware, db_url=settings.SQLALCHEMY_DATABASE_URI)

    # Global dependencies
    app.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    app.azure_storage_client = AzureBlobStorageClient()
    app.azure_ocr_client = AzureOCRClient()
    app.azure_cv_client = AzureCustomVisionClient()
    return app


app = setup_app()
