from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=4, max_length=32)