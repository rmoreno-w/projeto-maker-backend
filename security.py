from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)