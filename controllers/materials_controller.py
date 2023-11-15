from fastapi import APIRouter, Depends

from controllers.depends.user import get_user_with_role
from models.material import Material
from models.user import User

router = APIRouter()

@router.post("/")
async def create_material(material_data: Material, logged_in_user: User = Depends(get_user_with_role(['admin']))):
    await material_data.save()
    return {"details": "Material criado com sucesso"}

@router.get("/")
async def get_materials(logged_in_user: User = Depends(get_user_with_role(['admin']))):
    return await Material.objects.all()