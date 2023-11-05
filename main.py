from fastapi import FastAPI
from routes import router

app = FastAPI()

app.include_router(router, prefix='')

@app.get("/")
def read_root():
    return {"Hello": "World"}
