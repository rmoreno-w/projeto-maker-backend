import ormar
from config import database, metadata


class Address(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str ='addresses'

    id: int = ormar.Integer(primary_key=True)
    street: str = ormar.String(max_length=200)
    cep: str = ormar.String(max_length=10)
    number: int = ormar.Integer()
    district: str = ormar.String(max_length=200)
    city: str = ormar.String(max_length=200)
    state: str = ormar.String(max_length=200)
    complement: str = ormar.String(max_length=200, nullable=True)