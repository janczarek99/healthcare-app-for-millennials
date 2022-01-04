from fastapi import APIRouter, Depends

from src.healthcare_api.schemas.user import UserSchema
from src.healthcare_api.utils.authentication import current_user
from src.healthcare_api.utils.enums import CustomVisionModels

router = APIRouter(tags=["Photos"])


@router.get("/models")
async def get_available_models(_: UserSchema = Depends(current_user)):
    return CustomVisionModels.get_names()
