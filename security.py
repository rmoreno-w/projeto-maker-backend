import os
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

SECRET_KEY = os.getenv('SECRET_KEY', '123123123')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS512')
ACCESS_TOKEN_EXPIRE_HOURS = 24

def create_jwt_token(subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode = {"exp": expire, "sub": str(subject)} #sub = id do usuário, aqui é o que vai ser encodado -> Data + id

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS512')
    return encoded_jwt