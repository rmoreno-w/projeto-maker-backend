import re

import ormar
from config import database, metadata
from pydantic import validator


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

    @validator('cep')
    def validate_cep_formatting(cls, value):
        if not re.compile('^\d{2}.\d{3}-\d{3}$').match(value):
            raise ValueError('Campo CEP inválido - Formato requerido: xx.xxx-xxx')
        return value
    
    @validator('district')
    def validate_district_formatting(cls, value):
        if not re.compile('^[A-Z]{2}$').match(value):
            raise ValueError('Campo Estado inválido - Formato requerido: Sigla de duas letras maiúsculas')
        return value