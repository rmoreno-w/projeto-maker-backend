from fastapi import APIRouter
from models.member import MakerMember

router = APIRouter()

@router.post("/")
async def create_member(member_data: MakerMember):
    await member_data.save()
    return member_data

@router.get("/")
async def get_members():
    return await MakerMember.objects.all()