from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    street: str
    cep: str
    number: str
    district: str
    city: str
    state: str
    complement: Optional[str] = None