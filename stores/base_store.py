from typing import TypeVar
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from startup.extensions import db

T = TypeVar('T')

class BaseStore:
    def commit(self):
        db.session.commit()

    def add(self, x: T) -> None:
        db.session.add(instance=x)
        db.session.commit()