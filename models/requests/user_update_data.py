from typing import Optional

from pydantic import BaseModel, Json


class UserUpdateData(BaseModel):
    email: Optional[str] = None
    activation_state: Optional[bool] = None
    password: Optional[str] = None
    phone_number: Optional[int] = None
    street: Optional[str] = None
    cep: Optional[str] = None
    house_number: Optional[int] = None
    district: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    complement: Optional[str] = None
    # role: Optional[Json] = None
