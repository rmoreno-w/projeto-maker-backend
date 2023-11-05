from typing import Optional, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Address(BaseModel):
    street: str
    cep: str
    number: str
    district: str
    city: str
    state: str
    complement: Optional[str] = None

class MakerMember(BaseModel):
    name: str
    cpf: str
    email: str
    address: Address
    activation_state: bool = True
    password: str

@app.post("/members")
def create_member(member_data: MakerMember):
    banco_de_dados.append(member_data)
    return member_data

@app.get("/members")
def get_members():
    return { "users": banco_de_dados }