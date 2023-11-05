import ormar
from config import database, metadata
from models.address import Address


class MakerMember(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'members'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    cpf: str = ormar.String(max_length=12)
    email: str = ormar.String(max_length=200)
    address: Address = ormar.ForeignKey(Address)
    activation_state: bool = ormar.Boolean(default=True)
    password: str = ormar.String(max_length=200)