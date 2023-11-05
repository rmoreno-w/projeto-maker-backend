import ormar
from fastapi import APIRouter, Response
from models.address import Address
from models.member import MakerMember

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