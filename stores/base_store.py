from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from startup.extensions import db


class BaseStore:
    def _commit(self) -> None:
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("A database integrity error occurred.") from e
        except SQLAlchemyError:
            db.session.rollback()
            raise