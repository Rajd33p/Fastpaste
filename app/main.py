from fastapi import FastAPI
from app.routes import paste

app = FastAPI()

app.include_router(paste.router)
