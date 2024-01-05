'This module is the entry point to the assignment project'

from fastapi import FastAPI 
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.routers.routes import router
from contextlib import asynccontextmanager


config = dotenv_values(".env")

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Connect to DB
    app.mongodb_client = MongoClient(config["ATLAS_URI"], server_api=ServerApi('1'))
    app.database = app.mongodb_client[config["DB_NAME"]]

    try:
        app.mongodb_client.admin.command('ping')
        print(f"Connected to staging DB ({config["DB_NAME"]}) successfully.")
    except Exception as e:
        print(e)

    yield

    # Shutdown connection
    app.mongodb_client.close()
    print(f"Disconnected from staging DB ({config["DB_NAME"]}) successfully.")


app = FastAPI(
    title = "Elevatus Technical Assignment",
    description = "Technical Assignment by Elevatus for a Python Developer Role",
    lifespan=lifespan
              )



app.include_router(router)