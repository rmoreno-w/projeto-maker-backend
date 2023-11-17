import ormar

from config import database, metadata


class Service(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'services'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    description: str = ormar.String(max_length=1200)
    base_price: int = ormar.Integer(minimum=0)