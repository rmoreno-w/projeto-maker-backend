from fastapi import APIRouter
from models.member import MakerMember

router = APIRouter()

banco_de_dados = [{
        "name": "Claudiomar",
        "cpf": "017660886888",
        "email": "claudio.mar@unif.ei",
        "address": {
            "street": "Rua Prefeito Leão Jhonson",
            "cep": "37800188",
            "number": "522",
            "district": "BPS",
            "city": "Itajubá",
            "state": "MG",
            "complement": ""
        },
        "activation_state": True,
        "password": "1234mil"
    }
]

@router.post("/")
def create_member(member_data: MakerMember):
    banco_de_dados.append(member_data)
    return member_data

@router.get("/")
def get_members():
    return { "users": banco_de_dados }