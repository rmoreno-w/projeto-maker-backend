import ormar
from fastapi import APIRouter, Response
from models.member import MakerMember
from models.requests.member_update_data import MemberUpdateData

router = APIRouter()

@router.post("/")
async def create_member(member_data: MakerMember):
    await member_data.address.save()
    await member_data.save()
    return member_data

@router.get("/")
async def get_members():
    return await MakerMember.objects.select_related('address').all()

@router.get("/{name_or_email}")
async def get_members_by_name_or_email(name_or_email: str, response: Response):
    users = await MakerMember.objects.select_related('address').all(name=name_or_email)
    if users != []:
        return users
    
    else:
        users = await MakerMember.objects.select_related('address').all(email=name_or_email)
        if users != []:
            return users
        else:
            return {"message": f"Usuário com nome ou email igual a '{name_or_email}' não encontrado na base de dados"}

@router.patch("/{member_id}")
async def update_member(member_id: int, response: Response, updated_fields: MemberUpdateData):
    try:
        existing_member = await MakerMember.objects.select_related('address').get(id=member_id)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        if "address" in fields_to_update:
            await existing_member.address.update(**fields_to_update["address"])
            del fields_to_update["address"]

        if len(fields_to_update) > 0:
            await existing_member.update(**fields_to_update)

        return existing_member

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Membro de id {member_id} não encontrado"}