from typing import List, Optional

from pydantic import BaseModel


class UserCheckByIdResponse(BaseModel):
    name: str
    street: str
    email: str
    cep: str
    district: str
    house_number: int
    phone_number: str
    city: str
    state: str
    complement: Optional[str] = None
    role: List[str]