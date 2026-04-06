from models.user import User
from startup.extensions import db
from stores.base_store import BaseStore

class AuthStore(BaseStore):
    def create_user(self, name: str, password_hash: str) -> User:
        user = User(name=name, password_hash=password_hash)
        db.session.add(user)
        self._commit()
        return user
    
    def get_user_by_name(self, name: str) -> User | None:
        return User.query.filter_by(name=name).first()

auth_store_instance = AuthStore()