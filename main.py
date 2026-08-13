from fastapi import FastAPI
from routes import crud, filtering
from database import Base, engine

app = FastAPI()

app.include_router(crud.router)
app.include_router(filtering.router)