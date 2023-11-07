from pydantic import BaseModel


class UserCreationResponse(BaseModel):
    name: str
    email: str