import re
from typing import Optional

import ormar
from pydantic import Json, validator

from config import database, metadata

valid_user_types = ['admin', 'member', 'customer']

class User(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename: str = 'users'

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=200)
    cpf: str = ormar.String(max_length=14)
    email: str = ormar.String(max_length=200, unique=True)
    activation_state: bool = ormar.Boolean(default=True)
    password: str = ormar.String(max_length=200)
    phone_number: str = ormar.String(max_length=11)
    street: str = ormar.String(max_length=200)
    cep: str = ormar.String(max_length=10)
    house_number: int = ormar.Integer()
    district: str = ormar.String(max_length=200)
    city: str = ormar.String(max_length=200)
    state: str = ormar.String(max_length=2)
    complement: str = ormar.String(max_length=200, nullable=True)
    unifei_registration_number: str = ormar.String(max_length=20, nullable=True)
    role: Optional[Json] = ormar.JSON(default=['customer'])
    is_user_deleted: bool = ormar.Boolean(default=False)

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

    @validator('cep')
    def validate_cep_formatting(cls, value):
        if not re.compile('^\d{2}.\d{3}-\d{3}$').match(value):
            raise ValueError('Campo CEP inválido - Formato requerido: xx.xxx-xxx')
        return value
    
    @validator('state')
    def validate_state_formatting(cls, value):
        if not re.compile('^[A-Z]{2}$').match(value):
            raise ValueError('Campo Estado inválido - Formato requerido: Sigla de duas letras maiúsculas')
        return value
    
    @validator('role')
    def validate_role_formatting(cls, roles_list):
        if not isinstance(roles_list, list):
            raise ValueError('As funçoes do usuário devem ser incluidas em uma lista/vetor')
        
        for role in roles_list:
            if not isinstance(role, str) or role not in valid_user_types:
                raise ValueError(f'A função {role} nao é valida')
        return roles_list
    
    @validator('role')
    def remove_duplicated_roles(cls, roles_list):
        return list(set(roles_list))