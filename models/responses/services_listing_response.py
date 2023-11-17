from typing import List, Optional

from pydantic import BaseModel


class ServiceInResponse(BaseModel):
    name: str
    description: str
    base_price: int