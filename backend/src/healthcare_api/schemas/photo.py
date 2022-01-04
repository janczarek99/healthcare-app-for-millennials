from uuid import UUID

from pydantic import BaseModel, Field

from src.healthcare_api.utils.enums import CustomVisionModels


class PhotoSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: UUID
    user_id: int = Field(..., alias="userId", exclude=True)
    name: str
    blob_path: str = Field(..., alias="blobPath")
    model_type: CustomVisionModels = Field(..., alias="modelType")
    model_result: str = Field(..., alias="modelResult")

    @property
    def blob_id(self) -> UUID:
        return UUID(self.blob_path.split("/")[-1])
