from models.user import User
from request_models.register_request import RegisterRequest
from stores.auth_store import AuthStore, auth_store_instance
from werkzeug.security import generate_password_hash


class AuthRepository:
    def __init__(self, auth_store: AuthStore):
        self.auth_store = auth_store
        
    def register_user(self, reg_req: RegisterRequest) -> User:
        existing = self.auth_store.get_user_by_name(reg_req.name)
        if existing:
            raise ValueError(f"Username '{reg_req.name}' is already taken.")

        password_hash = generate_password_hash(reg_req.password)
        return self.auth_store.create_user(name=reg_req.name, password_hash=password_hash)

auth_repository_instance = AuthRepository(auth_store=auth_store_instance)