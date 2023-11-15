from typing import Optional

from pydantic import BaseModel


class MaterialUpdateData(BaseModel):
    name: Optional[str] = None
    description:  Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None