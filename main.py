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
    #Executed before the app starts
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        print(database_.is_connected)

    yield

    #Executed after shutdown
    database_ = app.state.database
    print(database_)
    if database_.is_connected:
        await database_.disconnect()

port = 8000
app = FastAPI(callbacks= print(f"Server online! Ouvindo na porta {port}"), lifespan=lifespan)

metadata = config.metadata
database = config.database
app.state.database = database

app.include_router(router, prefix='')