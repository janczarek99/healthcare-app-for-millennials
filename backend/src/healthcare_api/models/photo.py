from typing import List, Optional
from uuid import uuid4

from fastapi_sqlalchemy import db
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError

from .base import Base
from ..schemas.photo import PhotoSchema
from ..utils.enums import CustomVisionModels
from ...exceptions import CannotCreateObjectException


class Photo(Base):
    __tablename__ = "photos"

    MEDIUM_SIZE_STR = 255

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(MEDIUM_SIZE_STR), nullable=False)
    blob_path = Column(String(MEDIUM_SIZE_STR), nullable=False)
    model_type = Column(Enum(CustomVisionModels), nullable=False)
    model_result = Column(String(MEDIUM_SIZE_STR))

    @classmethod
    def get_photos_for_user(cls, user_id: int, options=None) -> List[PhotoSchema]:
        query = cls.get_configured_query(None)
        query = query.where(cls.user_id == user_id)

        results = db.session.execute(query)

        photos_db = results.unique().scalars().all()

        photos = [PhotoSchema.from_orm(photo_db) for photo_db in photos_db]
        return photos

    @classmethod
    def get_photo_by_id(cls, photo_id: UUID, options=None) -> Optional[PhotoSchema]:
        query = cls.get_configured_query(None)
        query = query.where(cls.id == photo_id)

        results = db.session.execute(query)

        photo_db = results.unique().scalars().first()

        return PhotoSchema.from_orm(photo_db)

    @classmethod
    def add(
        cls, user_id: int, name: str, blob_path: str, model_type: CustomVisionModels, model_result: str
    ) -> PhotoSchema:
        new_photo = Photo(
            user_id=user_id,
            name=name,
            blob_path=blob_path,
            model_type=model_type,
            model_result=model_result,
        )

        try:
            db.session.add(new_photo)
            db.session.commit()
            db.session.refresh(new_photo)
            return PhotoSchema.from_orm(new_photo)
        except IntegrityError:
            db.session.rollback()
            raise CannotCreateObjectException
