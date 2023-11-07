import ormar
from fastapi import APIRouter, Depends, Form, HTTPException, Response

from controllers.depends.user import get_logged_in_user
from models.requests.user_update_data import UserUpdateData
from models.responses.user_create_response import UserCreationResponse
from models.user import User
from security import create_jwt_token, encrypt_password, verify_password

router = APIRouter()

@router.post("/", response_model=UserCreationResponse)
async def create_user(user_data: User):
    user_data.password = encrypt_password(user_data.password)
    await user_data.save()
    return user_data

@router.get("/")
async def get_users(logged_in_user: User = Depends(get_logged_in_user)):
    return await User.objects.all()

@router.get("/{name_or_email}")
async def get_users_by_name_or_email(name_or_email: str, response: Response, logged_in_user: User = Depends(get_logged_in_user)):
    users = await User.objects.all(name=name_or_email)
    if users != []:
        return users
    
    else:
        users = await User.objects.all(email=name_or_email)
        if users != []:
            return users
        else:
            response.status_code = 404
            return {"message": f"Usuário com nome ou email igual a '{name_or_email}' não encontrado na base de dados"}

@router.patch("/{user_id}")
async def update_user(user_id: int, response: Response, updated_fields: UserUpdateData, logged_in_user: User = Depends(get_logged_in_user)):
    try:
        existing_user = await User.objects.get(id=user_id)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        if "password" in fields_to_update:
            existing_user.password = encrypt_password(fields_to_update["password"])

        if len(fields_to_update) > 0:
            await existing_user.update(**fields_to_update)

        return existing_user

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Usuário de id {user_id} não encontrado"}

@router.delete("/{user_id}")
async def delete_user(user_id: int, response: Response, logged_in_user: User = Depends(get_logged_in_user)):
    try:
        existing_user = await User.objects.get(id=user_id)

        await existing_user.delete()

        return {"message": "Usuário removido com sucesso"}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Usuário de id {user_id} não encontrado"}

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await User.objects.get_or_none(email=username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="Email ou senha incorreto(s)")

    return {
        "access_token": create_jwt_token(user.id),
        "token_type": "bearer"
    }
#login@user.com poderosa123