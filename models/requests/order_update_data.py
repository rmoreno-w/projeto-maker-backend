from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from models.service_in_order import ServiceInOrder


class OrderUpdateData(BaseModel):
    services: Optional[List[ServiceInOrder]] = None
    payment_status: Optional[str] = None
    price: Optional[float] = None
    order_status: Optional[str] = None
    paid_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None