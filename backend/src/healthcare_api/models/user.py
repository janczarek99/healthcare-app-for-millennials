from typing import Optional, List

from fastapi_sqlalchemy import db
from sqlalchemy import Column, String, Integer, select, Boolean
from sqlalchemy.exc import IntegrityError

from .base import Base
from ..schemas.user import UserSchema
from ...exceptions import CreateUserException


class User(Base):
    __tablename__ = "users"

    MEDIUM_SIZE_STR = 255

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(MEDIUM_SIZE_STR), nullable=False)
    password = Column(String(MEDIUM_SIZE_STR), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    @classmethod
    def get_user_by_username(cls, username: str, options=None) -> Optional[UserSchema]:
        query = cls.get_configured_query(None)
        query = query.where(cls.username == username)

        results = db.session.execute(query)

        user = results.unique().scalars().first()

        return user

    @classmethod
    def add(cls, username: str, password: str) -> UserSchema:
        if username in cls._get_all_usernames():
            raise CreateUserException(username)

        new_user = User(username=username, password=password)
        db.session.add(new_user)

        try:
            db.session.commit()
            db.session.refresh(new_user)
            return UserSchema.from_orm(new_user)
        except IntegrityError:
            db.session.rollback()
            raise CreateUserException(username)

    @classmethod
    def _get_all_usernames(cls) -> List[str]:
        results = db.session.execute(select(cls.username))
        usernames = results.unique().scalars().all()
        return usernames
