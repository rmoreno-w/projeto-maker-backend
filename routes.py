from fastapi import APIRouter

from controllers import consume_material_controller as consume_material
from controllers import materials_controller as materials
from controllers import orders_controller as orders
from controllers import reports_controller as reports
from controllers import service_in_order_controller as service_in_order
from controllers import services_controller as services
from controllers import teams_controller as teams
from controllers import users_controller as users

router = APIRouter()

router.include_router(users.router, prefix='/users', tags=['Usuários'])
router.include_router(materials.router, prefix='/materials', tags=['Materiais'])
router.include_router(services.router, prefix='/services', tags=['Serviços'])
router.include_router(orders.router, prefix='/orders', tags=['Pedidos'])
router.include_router(service_in_order.router, prefix='/services_in_orders', tags=['Serviços nos Pedidos'])
router.include_router(teams.router, prefix='/teams', tags=['Equipes'])
router.include_router(reports.router, prefix='/reports', tags=['Relatórios'])
router.include_router(consume_material.router, prefix='/consume', tags=['Consumir Materiais'])