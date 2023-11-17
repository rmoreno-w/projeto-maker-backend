from fastapi import APIRouter

from controllers import materials_controller as materials
from controllers import services_controller as services
from controllers import users_controller as users

router = APIRouter()

router.include_router(users.router, prefix='/users', tags=['Usuários'])
router.include_router(materials.router, prefix='/materials', tags=['Materiais'])
router.include_router(services.router, prefix='/services', tags=['Serviços'])