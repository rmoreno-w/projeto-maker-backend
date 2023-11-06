from typing import Optional

from pydantic import BaseModel


class AddressUpdateData(BaseModel):
    street: Optional[str] = None
    cep: Optional[str] = None
    number: Optional[int] = None
    district: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    complement: Optional[str] = None