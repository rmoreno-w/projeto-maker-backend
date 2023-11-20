import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.order import Order
from models.requests.order_update_data import OrderUpdateData
from models.user import User

router = APIRouter()

@router.post("/")
async def create_order(order_data: Order , logged_in_user: User = Depends(get_user_with_role([]))):
    await order_data.save()
    return {"details": "Pedido criado com sucesso"}

@router.get("/")
async def get_orders(logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    return await Order.objects.all()

@router.patch("/{order_id}")
async def update_material(order_id: int, response: Response, updated_fields: OrderUpdateData, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    # print(logged_in_user)
    try:
        existing_order = await Order.objects.get(id=order_id)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        print(fields_to_update)
        if len(fields_to_update) > 0:
            await existing_order.update(**fields_to_update)

        edited_fields = str(list(fields_to_update.keys()))
        return {"message": f'{edited_fields} editado(s) com sucesso'}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Pedido de id {order_id} não encontrado"}
