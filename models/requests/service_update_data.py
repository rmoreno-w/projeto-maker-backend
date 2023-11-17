from typing import Optional

from pydantic import BaseModel


class ServiceUpdateData(BaseModel):
    name: Optional[str] = None
    description:  Optional[str] = None
    base_price: Optional[float] = None