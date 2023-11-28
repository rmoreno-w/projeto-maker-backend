import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.material import Material
from models.material_consumed_in_service import MaterialConsumedInService
from models.user import User

router = APIRouter()

@router.post("/")
async def consume_material(consumed_material: MaterialConsumedInService, response: Response, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    try:
        material = await Material.objects.get(id=consumed_material.material_id, is_material_deleted=False)
        await consumed_material.save()

        material.quantity = material.quantity - consumed_material.quantity
        await material.update()

        return {"details": f"{consumed_material.quantity} de {material.name} consumido no serviço {consumed_material.service_in_order_id.id}"}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Material de id {consumed_material.material_id} não encontrado"}

# @router.get("/")
# async def get_services_in_order(logged_in_user: User = Depends(get_user_with_role([]))):
#     # x = (await Order.objects.select_all().all())
#     # x = (await Order.objects.select_related("services").all())
#     # x = await ServiceInOrder.objects.select_all().order_by('service_id__id').all()
#     x = await ServiceInOrder.objects.select_all().order_by('id').all()
#     # select_related('service_in_order').all())
#     return x
#     # return await Order.objects.select_related('service_in_order').all()


# @router.patch("/{service_id}")
# async def update_service(service_id: int, response: Response, updated_fields: ServiceUpdateData, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
#     # print(logged_in_user)
#     try:
#         existing_service = await Service.objects.get(id=service_id, is_service_available=True)

#         fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

#         if "base_price" in fields_to_update:
#             print(int(fields_to_update["base_price"] * 100))
#             fields_to_update["base_price"] = int(fields_to_update["base_price"] * 100)

#         if len(fields_to_update) > 0:
#             await existing_service.update(**fields_to_update)

#         edited_fields = str(list(fields_to_update.keys()))
#         return {"message": f'{edited_fields} editado(s) com sucesso'}

#     except ormar.exceptions.NoMatch:
#         response_status_code = 404
#         response.status_code = response_status_code
#         return {"message" : f"Serviço de id {service_id} não encontrado"}

# @router.delete("/{service_id}")
# async def delete_material(service_id: int, response: Response, logged_in_user: User = Depends(get_user_with_role(roles=['admin']))):
#     try:
#         existing_service = await Service.objects.get(id=service_id)

#         existing_service.is_service_available = False
#         await existing_service.update()

#         return {"message": "Serviço removido com sucesso"}

#     except ormar.exceptions.NoMatch:
#         response_status_code = 404
#         response.status_code = response_status_code
#         return {"message" : f"Serviço de id {service_id} não encontrado"}