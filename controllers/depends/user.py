from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from models.member import MakerMember
from pydantic import BaseModel, ValidationError
from security import JWT_ALGORITHM, SECRET_KEY


class TokenPayload(BaseModel):
    sub: Optional[int] #id do user
    exp: Optional[int]

# Variável q diz ao fastapi qual é a rota que faz auth e adiciona opçao de auth na documentação
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/members/login") 

# Verifica através do token da requisiçao se o usuário está autenticado
async def get_logged_in_user(token: str = Depends(reusable_oauth2)) -> MakerMember:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException (status_code=403, detail="Credenciais inválidas") # Ou id nao existe ou token expirado
    
    user = await MakerMember.objects.get_or_none(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # Usuário pode ter sido apagado após token ser emitido

    return user