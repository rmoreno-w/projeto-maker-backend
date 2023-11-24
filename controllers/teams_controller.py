import ormar
from fastapi import APIRouter, Depends, Response

from controllers.depends.user import get_user_with_role
from models.team import Team
from models.user import User

router = APIRouter()

@router.post("/")
async def create_team(team_data: Team, logged_in_user: User = Depends(get_user_with_role(['admin']))):
    await team_data.save()
    return {"details": "Equipe criado com sucesso", "id" : f"{team_data.id}"}

@router.get("/")
async def get_teams(logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    return await Team.objects.all(is_team_deleted=False)

# @router.patch("/{material_id}")
# async def update_material(material_id: int, response: Response, updated_fields: MaterialUpdateData, logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
#     # print(logged_in_user)
#     try:
#         existing_material = await Material.objects.get(id=material_id)

#         fields_to_update = updated_fields.dict(exclude_unset=True) #Pega as propriedades que vieram da requisição, não inclui as não presentes

#         if len(fields_to_update) > 0:
#             await existing_material.update(**fields_to_update)

#         edited_fields = str(list(fields_to_update.keys()))
#         return {"message": f'{edited_fields} editado(s) com sucesso'}

#     except ormar.exceptions.NoMatch:
#         response_status_code = 404
#         response.status_code = response_status_code
#         return {"message" : f"Material de id {material_id} não encontrado"}

@router.delete("/{team_id}")
async def delete_team(team_id: int, response: Response, logged_in_user: User = Depends(get_user_with_role(roles=['admin']))):
    try:
        existing_team = await Team.objects.get(id=team_id)

        existing_team.is_team_deleted = True
        await existing_team.update()

        return {"message": "Equipe removida com sucesso"}

    except ormar.exceptions.NoMatch:
        response_status_code = 404
        response.status_code = response_status_code
        return {"message" : f"Equipe de id {team_id} não encontrado"}