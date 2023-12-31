from datetime import datetime

import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.order import Order
from models.requests.order_update_data import OrderUpdateData
from models.service import Service
from models.service_in_order import ServiceInOrder
from models.user import User

router = APIRouter()

@router.post("/")
# async def create_order(order_data: Order, logged_in_user: User = Depends(get_user_with_role([]))):
async def create_order(order_data: list[ServiceInOrder], logged_in_user: User = Depends(get_user_with_role([]))):
    newOrder = await Order(customer_id=logged_in_user.id, solicited_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price=0).save()

    services = await Service.objects.all(is_service_available=True)

    for service in order_data:
        service_index_in_services_array = services.index(service.service_id) # .index acha o elemento que tenha como índice o que voce passa como parametro 
        found_service = services[service_index_in_services_array]            # Achando a Entidade do serviço com index igual ao do serviço recebido na chamada http

        service.order_id = newOrder.id                                       # Ligando o serviço ao pedido
        service.service_base_price = found_service.base_price                # Igualando o preco base do servico no pedido ao preço base da Entidade serviço
        newOrder.price += service.service_base_price                         # Somando o preço do serviço no preço do pedido
        await service.save()

    await newOrder.update()
    return {"details": "Pedido criado com sucesso"}

@router.get("/")
async def get_orders(logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    return await Order.objects.select_related('services').all()

@router.get("/my_orders")
async def get_my_orders(logged_in_user: User = Depends(get_user_with_role(['customer']))):
    return await Order.objects.select_related('services').filter(customer_id=logged_in_user.id).all()
    # return await ServiceInOrder.objects.select_all().order_by('id').all(order_id__customer_id=logged_in_user.id)

@router.patch("/{order_id}")
async def update_order(order_id: int, response: Response, updated_fields: OrderUpdateData, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    print(updated_fields)
    try:
        existing_order = await Order.objects.get(id=order_id)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        if len(fields_to_update) > 0:
            await existing_order.update(**fields_to_update)

        if "services" in fields_to_update:
            for service in fields_to_update['services']:
                existing_service_in_order = await ServiceInOrder.objects.get(id=service['id'])
                await existing_service_in_order.update(**service)
                
        edited_fields = str(list(fields_to_update.keys()))
        return {"message": f'{edited_fields} editado(s) com sucesso'}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Pedido de id {order_id} não encontrado"}
