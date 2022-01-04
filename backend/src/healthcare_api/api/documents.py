from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File

from src.deps import get_azure_storage_client, get_azure_ocr_client
from src.exceptions import UnauthorizedException
from src.healthcare_api.schemas.user import UserSchema
from src.healthcare_api.utils.authentication import current_user
from src.healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from src.healthcare_api.utils.azure_ocr_client import AzureOCRClient
from src.healthcare_api.utils.enums import AzureStorageEntityTypes

router = APIRouter(tags=["Documents"])


@router.get("/documents")
async def get_all_documents(user: UserSchema = Depends(current_user)):
    return [
        {
            "id": "1",
            "name": "Brain X-ray Doctor XXX opinion",
            "blob_path": "/{user_id}/documents/{doc_id}.jpg",
            "text_value": "OCRed text...[:30]",
            "minified_img": "base64xxxxxxx"
        },
        {
            "id": "2",
            "name": "Medical history before lung X-ray",
            "blob_path": "/{user_id}/documents/{doc_id}.jpg",
            "text_value": "Another OCRed text...[:30]",
            "minified_img": "base64xxxxxxx"
        }
    ]


@router.get("/documents/{document_id}")
async def get_document(
    document_id: UUID,
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    user: UserSchema = Depends(current_user)
):
    # Get one doc from db
    try:
        # file = azure_storage_client.download_file(
        #     user_id=user.id, entity=AzureStorageEntityTypes.DOCUMENTS.value, entity_id=document_id
        # )
        file = "base64XXXX"
    except Exception:
        file = None

    return {"image": file, "other": "", "properties": ""}


@router.post("/documents")
async def add_new_document(
    uploaded_file: UploadFile = File(..., alias="uploadedFile"),
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    azure_ocr_client: AzureOCRClient = Depends(get_azure_ocr_client),
    user: UserSchema = Depends(current_user)
):
    blob_path = azure_storage_client.upload_file(
        user_id=user.id, entity=AzureStorageEntityTypes.DOCUMENTS.value, file=uploaded_file.file
    )

    ocr_text = azure_ocr_client.get_text_from_image(file=uploaded_file.file)

    # Add to DB

    return {"blob": blob_path, "ocr": ocr_text}

