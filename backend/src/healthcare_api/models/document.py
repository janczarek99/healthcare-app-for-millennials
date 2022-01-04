from typing import List, Optional
from uuid import uuid4

from fastapi_sqlalchemy import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError

from .base import Base
from ..schemas.document import DocumentSchema
from ...exceptions import CannotCreateObjectException


class Document(Base):
    __tablename__ = "documents"

    MEDIUM_SIZE_STR = 255
    VERY_LONG_STR = 10000

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(MEDIUM_SIZE_STR), nullable=False)
    blob_path = Column(String(MEDIUM_SIZE_STR), nullable=False)
    ocred_text = Column(String(VERY_LONG_STR), nullable=False)

    @classmethod
    def get_documents_for_user(cls, user_id: int, options=None) -> List[DocumentSchema]:
        query = cls.get_configured_query(None)
        query = query.where(cls.user_id == user_id)

        results = db.session.execute(query)

        documents_db = results.unique().scalars().all()

        documents = [DocumentSchema.from_orm(document_db) for document_db in documents_db]
        return documents

    @classmethod
    def get_document_by_id(cls, document_id: UUID, options=None) -> Optional[DocumentSchema]:
        query = cls.get_configured_query(None)
        query = query.where(cls.id == document_id)

        results = db.session.execute(query)

        document_db = results.unique().scalars().first()

        return DocumentSchema.from_orm(document_db)

    @classmethod
    def add(cls, user_id: int, name: str, blob_path: str, ocred_text: str) -> DocumentSchema:
        new_document = Document(
            user_id=user_id, name=name, blob_path=blob_path, ocred_text=ocred_text
        )

        try:
            db.session.add(new_document)
            db.session.commit()
            db.session.refresh(new_document)
            return DocumentSchema.from_orm(new_document)
        except IntegrityError:
            db.session.rollback()
            raise CannotCreateObjectException
