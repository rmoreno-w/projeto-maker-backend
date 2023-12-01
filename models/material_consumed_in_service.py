import ormar

from config import database, metadata
from models.material import Material
from models.service_in_order import ServiceInOrder


class MaterialConsumedInService(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'material_consumed_in_service'

    id: int = ormar.Integer(primary_key=True)
    material_id: int = ormar.ForeignKey(to=Material, skip_reverse=True, related_name='materials')
    service_in_order_id: int = ormar.ForeignKey(to=ServiceInOrder, skip_reverse=False, related_name='materials')
    quantity: float = ormar.Float(minimum=0)