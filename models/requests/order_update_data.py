from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderUpdateData(BaseModel):
    payment_status: Optional[str] = None
    price: Optional[float] = None
    order_status: Optional[str] = None
    paid_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None