import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.order import Order
from models.requests.material_update_data import MaterialUpdateData
from models.user import User

router = APIRouter()

@router.post("/")
async def create_order(order_data: Order , logged_in_user: User = Depends(get_user_with_role([]))):
    await order_data.save()
    return {"details": "Pedido criado com sucesso"}