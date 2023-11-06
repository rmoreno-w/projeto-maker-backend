from typing import Optional

from models.requests.address_update_data import AddressUpdateData
from pydantic import BaseModel


class MemberUpdateData(BaseModel):
    email: Optional[str] = None
    address: Optional[AddressUpdateData] = None
    activation_state: Optional[bool] = None
    password: Optional[str] = None