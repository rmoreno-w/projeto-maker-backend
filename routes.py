from fastapi import APIRouter

from controllers import materials_controller as materials
from controllers import orders_controller as orders
from controllers import service_in_order_controller as service_in_order
from controllers import services_controller as services
from controllers import users_controller as users

router = APIRouter()

router.include_router(users.router, prefix='/users', tags=['Usuários'])
router.include_router(materials.router, prefix='/materials', tags=['Materiais'])
router.include_router(services.router, prefix='/services', tags=['Serviços'])
router.include_router(orders.router, prefix='/orders', tags=['Pedidos'])
router.include_router(service_in_order.router, prefix='/services_in_orders', tags=['Serviços nos Pedidos'])