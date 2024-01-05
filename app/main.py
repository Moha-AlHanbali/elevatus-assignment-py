'This module is the entry point to the assignment project'

from fastapi import FastAPI
from app.routers.routes import router

app = FastAPI()

app.include_router(router)