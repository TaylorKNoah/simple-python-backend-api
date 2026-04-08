from models.user import User
from request_models.register_request import RegisterRequest
from stores.auth_store import AuthStore, auth_store_instance
from werkzeug.security import check_password_hash, generate_password_hash


class AuthRepository:
    def __init__(self, auth_store: AuthStore):
        self.auth_store = auth_store
        
    def register_user(self, reg_req: RegisterRequest) -> User:
        existing = self.auth_store.get_user_by_name(reg_req.name)
        if existing:
            raise ValueError(f"Username '{reg_req.name}' is already taken.")

        password_hash = generate_password_hash(reg_req.password)
        return self.auth_store.create_user(name=reg_req.name, password_hash=password_hash)


    def login_user(self, name: str, password: str):
        # does user exist?
        user: User = self.auth_store.get_user_by_name(name)
        if not user:
            raise ValueError("Invalid Credentials.")
        
        # is password correct?
        is_valid_password = check_password_hash(user.password_hash, password)
        if not is_valid_password:
            raise ValueError("Invalid Credentials.")
        
        return user


auth_repository_instance = AuthRepository(auth_store=auth_store_instance)