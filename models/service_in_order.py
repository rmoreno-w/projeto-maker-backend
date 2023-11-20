
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
    order_id: int = ormar.ForeignKey(to=Order, skip_reverse=True)
    service_id: int = ormar.ForeignKey(to=Service, skip_reverse=True)
    service_price: float | None = ormar.Float(minimum=0, nullable=True)
    service_data: Json | None = ormar.JSON(nullable=True)
