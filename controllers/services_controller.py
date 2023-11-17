from typing import List

import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
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
    return await Service.objects.all()
