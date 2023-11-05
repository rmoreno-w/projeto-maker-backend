"""
Comando pra exportar dependências do Python: pip freeze > requirements.txt, vai todas deps pro txt
pra instalar -> pip install requirements.txt
"""

from contextlib import asynccontextmanager

import config
from fastapi import FastAPI
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Método que inicializa database, utilizando ciclo de vida do servidor

    #Executado antes de Inicializar o servidor
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

    yield

    #Executado após desligar o servidor
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

port = 8000
app = FastAPI(callbacks= print(f"Server online! Ouvindo na porta {port}"), lifespan=lifespan)

metadata = config.metadata
database = config.database
app.state.database = database

app.include_router(router, prefix='')