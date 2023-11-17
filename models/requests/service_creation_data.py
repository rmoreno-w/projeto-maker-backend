from pydantic import BaseModel


class ServiceCreationData(BaseModel):
    name: str
    description:  str
    base_price: float