from pydantic import BaseModel

class LoginResponse(BaseModel):
    jwt_token: str