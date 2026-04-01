from models.user import User
from request_models.register_request import RegisterRequest
from stores.auth_store import auth_store
from werkzeug.security import generate_password_hash


class AuthRepository:
    def register_user(self, reg_req: RegisterRequest) -> User:
        existing = auth_store.get_user_by_name(reg_req.name)
        if existing:
            raise ValueError(f"Username '{reg_req.name}' is already taken.")

        password_hash = generate_password_hash(reg_req.password)
        return auth_store.create_user(name=reg_req.name, password_hash=password_hash)

auth_repository = AuthRepository()