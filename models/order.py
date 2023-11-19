from datetime import datetime
from enum import Enum
from typing import Optional

import ormar
from pydantic import validator

from config import database, metadata
from models.user import User

valid_payment_status = ['Unpaid', 'In analysis', 'Paid']
valid_order_status = ['In analysis', 'Awaiting for approval', 'Not approved', 'Approved', 'To do', 'In progress', 'Done', 'Delivered']

class PaymentStatus(Enum):
    unpaid = 'Unpaid'
    in_analysis = 'In analysis'
    paid = 'Paid'

class OrderStatus(Enum):
    in_analysis = 'In analysis'
    awaiting_for_approval = 'Awaiting for approval'
    not_approved = 'Not approved'
    approved = 'Approved'
    to_do = 'To do'
    in_progress = 'In progress'
    done = 'Done'
    delivered = 'Delivered'

class Order(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'orders'

    id: int = ormar.Integer(primary_key=True)
    customer_id: int = ormar.ForeignKey(to=User, skip_reverse=True)
    payment_status: str = ormar.String(max_length=25, choices=list(PaymentStatus), default='Unpaid')
    price: float = ormar.Float(minimum=0)
    order_status: str = ormar.String(max_length=25, choices=list(OrderStatus), default='In analysis')
    solicited_at: datetime = ormar.DateTime(timezone=True, default=datetime.time)
    paid_at: datetime | None = ormar.DateTime(nullable=True)
    started_at: datetime | None = ormar.DateTime(nullable=True)
    finished_at: datetime | None = ormar.DateTime(nullable=True)
    delivered_at: datetime | None = ormar.DateTime(nullable=True)

    @validator('payment_status')
    def validate_payment_status_formatting(cls, payment_status):
        if not isinstance(payment_status, str) or payment_status not in valid_payment_status:
            raise ValueError(f'O status de pagamento {payment_status} nao é valido')
        return payment_status

    @validator('order_status')
    def validate_order_status_formatting(cls, order_status):
        if not isinstance(order_status, str) or order_status not in valid_order_status:
            raise ValueError(f'O status de pedido {order_status} nao é valido')
        return order_status