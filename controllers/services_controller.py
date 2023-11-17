from typing import List

import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.requests.service_update_data import ServiceUpdateData
from models.responses.services_listing_response import ServiceInResponse
from models.service import Service
from models.user import User

router = APIRouter()

@router.post("/")
async def create_service(service_data: Service, logged_in_user: User = Depends(get_user_with_role(['admin']))):
    await service_data.save()
    return {"details": "Serviço criado com sucesso", "id" : f"{service_data.id}"}

@router.get("/", response_model=List[ServiceInResponse])
async def get_services(logged_in_user: User = Depends(get_user_with_role([]))):
    return await Service.objects.all(is_service_available=True)


@router.patch("/{service_id}")
async def update_service(service_id: int, response: Response, updated_fields: ServiceUpdateData, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    # print(logged_in_user)
    try:
        existing_service = await Service.objects.get(id=service_id, is_service_available=True)

        fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

        if len(fields_to_update) > 0:
            await existing_service.update(**fields_to_update)

        edited_fields = str(list(fields_to_update.keys()))
        return {"message": f'{edited_fields} editado(s) com sucesso'}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Serviço de id {service_id} não encontrado"}

@router.delete("/{service_id}")
async def delete_material(service_id: int, response: Response, logged_in_user: User = Depends(get_user_with_role(roles=['admin']))):
    try:
        existing_service = await Service.objects.get(id=service_id)

        existing_service.is_service_available = False
        await existing_service.update()

        return {"message": "Serviço removido com sucesso"}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Serviço de id {service_id} não encontrado"}