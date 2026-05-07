from models.user import User
from stores.base_store import BaseStore

class AuthStore(BaseStore):
    def create_user(self, user: User) -> None:
        self.add(user)
        sdfsdf
    
    def get_user_by_name(self, name: str) -> User | None:
        return User.query.filter_by(name=name).first()

auth_store_instance = AuthStore()