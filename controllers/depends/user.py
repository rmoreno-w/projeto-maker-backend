from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError

from models.user import User
from security import JWT_ALGORITHM, SECRET_KEY


class TokenPayload(BaseModel):
    sub: Optional[int] #id do user
    exp: Optional[int]

# Variável q diz ao fastapi qual é a rota que faz auth e adiciona opçao de auth na documentação
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login") 

# Verifica através do token da requisiçao se o usuário está autenticado
async def get_logged_in_user(token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

    except (jwt.JWTError, ValidationError):
        raise HTTPException (status_code=403, detail="Credenciais inválidas") # Ou id nao existe ou token expirado
    
    user = await User.objects.get_or_none(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # Usuário pode ter sido apagado após token ser emitido

    return user


# Verifica através do token da requisiçao se o usuário está autenticado
def get_user_with_role(roles: List[str] = []):
    def inner(logged_in_user: User = Depends(get_logged_in_user)) -> User:
        # Se a lista de funções for vazia, qualquer usuário pode acessar
        if not len(roles):
            return logged_in_user
        
        # Se a lista de funções nao for vazia, percorrer as funcoes que dao acesso ao recurso e ver se o usuário tem essa funcao no seu vetor de funcoes
        for role in roles:
            if role in logged_in_user.role:
                return logged_in_user
            
        raise HTTPException(
            status_code=403, detail='O usuário não possui permissão para acessar '
        )
    return inner