from uuid import UUID

from pydantic import BaseModel, Field


class DocumentSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    id: UUID
    user_id: int = Field(..., alias="userId", exclude=True)
    name: str
    blob_path: str = Field(..., alias="blobPath")
    ocred_text: str = Field(..., alias="ocredText")

    @property
    def blob_id(self) -> UUID:
        return UUID(self.blob_path.split("/")[-1])
