from fastapi import Request
from passlib.context import CryptContext

from src.healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from src.healthcare_api.utils.azure_custom_vision_client import AzureCustomVisionClient
from src.healthcare_api.utils.azure_ocr_client import AzureOCRClient


async def get_pwd_context(request: Request) -> CryptContext:
    return request.app.pwd_context


async def get_azure_storage_client(request: Request) -> AzureBlobStorageClient:
    return request.app.azure_storage_client


async def get_azure_ocr_client(request: Request) -> AzureOCRClient:
    return request.app.azure_ocr_client


async def get_azure_cv_client(request: Request) -> AzureCustomVisionClient:
    return request.app.azure_cv_client
