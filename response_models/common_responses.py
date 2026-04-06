from pydantic import BaseModel


class ErrorResponse(BaseModel):
    ErrorMessage: str