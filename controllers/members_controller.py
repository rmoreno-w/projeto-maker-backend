import ormar
from controllers.depends.user import get_logged_in_user
from fastapi import APIRouter, Depends, Form, HTTPException, Response
from models.member import MakerMember
from models.requests.member_update_data import MemberUpdateData
from models.responses.member_create_response import UserCreationResponse
from security import create_jwt_token, encrypt_password, verify_password

router = APIRouter()

@router.post("/", response_model=UserCreationResponse)
async def create_member(member_data: MakerMember):
    member_data.password = encrypt_password(member_data.password)
    await member_data.address.save()
    await member_data.save()
    return member_data

@router.get("/")
async def get_members(logged_in_user: MakerMember = Depends(get_logged_in_user)):
    return await MakerMember.objects.select_related('address').all()

@router.get("/{name_or_email}")
async def get_members_by_name_or_email(name_or_email: str, response: Response, logged_in_user: MakerMember = Depends(get_logged_in_user)):
    users = await MakerMember.objects.select_related('address').all(name=name_or_email)
    if users != []:
        return users
    
    else:
        users = await MakerMember.objects.select_related('address').all(email=name_or_email)
        if users != []:
            return users
        else:
            response.status_code = 404
            return {"message": f"Usuário com nome ou email igual a '{name_or_email}' não encontrado na base de dados"}

@router.patch("/{member_id}")
async def update_member(member_id: int, response: Response, updated_fields: MemberUpdateData, logged_in_user: MakerMember = Depends(get_logged_in_user)):
    try:
        existing_member = await MakerMember.objects.select_related('address').get(id=member_id)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        if "address" in fields_to_update:
            await existing_member.address.update(**fields_to_update["address"])
            del fields_to_update["address"]

        if "password" in fields_to_update:
            existing_member.password = encrypt_password(fields_to_update["password"])

        if len(fields_to_update) > 0:
            await existing_member.update(**fields_to_update)

        return existing_member

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Membro de id {member_id} não encontrado"}

@router.delete("/{member_id}")
async def delete_member(member_id: int, response: Response, logged_in_user: MakerMember = Depends(get_logged_in_user)):
    try:
        existing_member = await MakerMember.objects.select_related('address').get(id=member_id)

        member_address = existing_member.address
        await existing_member.delete()

        if member_address:
            await member_address.delete()

        return {"message": "Membro maker removido com sucesso"}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Membro de id {member_id} não encontrado"}

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = await MakerMember.objects.get_or_none(email=username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="Email ou senha incorreto(s)")

    return {
        "access_token": create_jwt_token(user.id),
        "token_type": "bearer"
    }
#login@user.com poderosa123