
import ormar
from pydantic import Json

from config import database, metadata
from models.order import Order
from models.service import Service


class ServiceInOrder(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'service_in_order'

    id: int = ormar.Integer(primary_key=True)
    order_id: int = ormar.ForeignKey(to=Order, skip_reverse=False, related_name='services')
    service_id: int = ormar.ForeignKey(to=Service, skip_reverse=True)
    service_base_price: int | None = ormar.Integer(minimum=0, nullable=True)
    service_price: int | None = ormar.Integer(minimum=0, nullable=True)
    service_data: Json | None = ormar.JSON(nullable=True)
