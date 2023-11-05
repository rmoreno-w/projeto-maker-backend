from controllers import members_controller as members
from fastapi import APIRouter

router = APIRouter()

router.include_router(members.router, prefix='/members')