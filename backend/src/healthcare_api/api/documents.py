from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Body

from src.deps import get_azure_storage_client, get_azure_ocr_client
from src.healthcare_api.models import Document
from src.healthcare_api.schemas.user import UserSchema
from src.healthcare_api.utils.authentication import current_user
from src.healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from src.healthcare_api.utils.azure_ocr_client import AzureOCRClient
from src.healthcare_api.utils.enums import AzureStorageEntityTypes
from src.healthcare_api.utils.photos import convert_file_to_html_base64

router = APIRouter(tags=["Documents"])


@router.get("/documents")
async def get_all_documents(user: UserSchema = Depends(current_user)):
    documents = Document.get_documents_for_user(user_id=user.id)
    return documents


@router.get("/documents/{document_id}")
async def get_document(
    document_id: UUID,
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    user: UserSchema = Depends(current_user),
):
    document = Document.get_document_by_id(document_id=document_id)
    try:
        file = azure_storage_client.download_file(
            user_id=user.id,
            entity=AzureStorageEntityTypes.DOCUMENTS.value,
            entity_id=document.blob_id,
        )
        img_as_base64 = convert_file_to_html_base64(file)
        file.close()

    except Exception:
        img_as_base64 = None

    return img_as_base64


@router.post("/documents")
async def add_new_document(
    uploaded_file: UploadFile = File(..., alias="uploadedFile"),
    document_name: str = Body(..., alias="documentName"),
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    azure_ocr_client: AzureOCRClient = Depends(get_azure_ocr_client),
    user: UserSchema = Depends(current_user),
):
    blob_path = azure_storage_client.upload_file(
        user_id=user.id, entity=AzureStorageEntityTypes.DOCUMENTS.value, file=uploaded_file.file
    )

    ocr_text = azure_ocr_client.get_text_from_image(file=uploaded_file.file)

    new_document = Document.add(
        user_id=user.id, name=document_name, blob_path=blob_path, ocred_text=ocr_text
    )

    return new_document
