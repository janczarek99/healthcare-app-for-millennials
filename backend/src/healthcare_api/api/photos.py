import json
from uuid import UUID

from fastapi import APIRouter, Depends, Body, UploadFile, File

from src.deps import get_azure_storage_client, get_azure_cv_client
from src.healthcare_api.models.photo import Photo
from src.healthcare_api.schemas.user import UserSchema
from src.healthcare_api.utils.authentication import current_user
from src.healthcare_api.utils.azure_blob_storage_client import AzureBlobStorageClient
from src.healthcare_api.utils.azure_custom_vision_client import AzureCustomVisionClient
from src.healthcare_api.utils.enums import CustomVisionModels, AzureStorageEntityTypes
from src.healthcare_api.utils.photos import convert_file_to_html_base64

router = APIRouter(tags=["Photos"])


@router.get("/models")
async def get_available_models(_: UserSchema = Depends(current_user)):
    return CustomVisionModels.get_names()


@router.get("/photos")
async def get_all_photos(user: UserSchema = Depends(current_user)):
    photos = Photo.get_photos_for_user(user_id=user.id)
    return photos


@router.get("/photos/{photo_id}")
async def get_photo(
    photo_id: UUID,
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    user: UserSchema = Depends(current_user),
):
    photo = Photo.get_photo_by_id(photo_id=photo_id)
    try:
        file = azure_storage_client.download_file(
            user_id=user.id,
            entity=AzureStorageEntityTypes.PHOTOS.value,
            entity_id=photo.blob_id,
        )
        img_as_base64 = convert_file_to_html_base64(file)
        file.close()

    except Exception:
        img_as_base64 = None

    return img_as_base64


@router.post("/photos")
async def add_new_photo(
    uploaded_file: UploadFile = File(..., alias="uploadedFile"),
    photo_name: str = Body(..., alias="photoName"),
    model_type: CustomVisionModels = Body(..., alias="modelType"),
    azure_storage_client: AzureBlobStorageClient = Depends(get_azure_storage_client),
    azure_cv_client: AzureCustomVisionClient = Depends(get_azure_cv_client),
    user: UserSchema = Depends(current_user),
):
    blob_path = azure_storage_client.upload_file(
        user_id=user.id, entity=AzureStorageEntityTypes.PHOTOS.value, file=uploaded_file.file
    )

    classification_results = azure_cv_client.classify_image_file(
        classification_model=model_type, file=uploaded_file.file
    )

    new_photo = Photo.add(
        user_id=user.id,
        name=photo_name,
        blob_path=blob_path,
        model_type=CustomVisionModels(model_type),
        model_result=json.dumps(classification_results),
    )

    return new_photo
