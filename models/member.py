import re

import ormar
from config import database, metadata
from models.address import Address
from pydantic import validator


class MakerMember(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'members'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    cpf: str = ormar.String(max_length=14)
    email: str = ormar.String(max_length=200)
    address: Address = ormar.ForeignKey(Address, skip_reverse=True)
    activation_state: bool = ormar.Boolean(default=True)
    password: str = ormar.String(max_length=200)

    @validator('cpf')
    def validate_cpf_formatting(cls, value):
        if not re.compile('^\d{3}.\d{3}.\d{3}-\d{2}$').match(value):
            raise ValueError('Campo CPF inválido - Formato requerido: xxx.xxx.xxx-xx')
        return value

    @validator('email')
    def validate_email_formatting(cls, value):
        if not re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$').match(value):
            raise ValueError('Campo email inválido, verifique por favor')
        return value