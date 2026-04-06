from pydantic import BaseModel

class RegisterResponse(BaseModel):
    id: int
    name: str