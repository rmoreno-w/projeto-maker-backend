from typing import Optional

from models.address import Address
from pydantic import BaseModel


class MakerMember(BaseModel):
    name: str
    cpf: str
    email: str
    address: Address
    activation_state: bool = True
    password: str