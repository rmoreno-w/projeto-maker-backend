from fastapi import APIRouter

from models.material import Material

router = APIRouter()

@router.post("/")
async def create_material(material_data: Material):
    await material_data.save()
    return {"details": "Material criado com sucesso"}