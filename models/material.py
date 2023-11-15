import ormar

from config import database, metadata


class Material(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'materials'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    description: str = ormar.String(max_length=200)
    quantity: float = ormar.Float(minimum=0)
    unit: str = ormar.String(max_length=200)