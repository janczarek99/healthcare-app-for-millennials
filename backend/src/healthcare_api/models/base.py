from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Query, joinedload


@as_declarative()
class Base:
    @classmethod
    def get_configured_query(cls, options: Optional[List]) -> Query:
        query = select(cls)
        if options is not None:
            for option in options:
                query = query.options(joinedload(option))

        return query
