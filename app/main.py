"This module is the entry point to the assignment project"

from fastapi import FastAPI
from app.routers.routes import router
from contextlib import asynccontextmanager

from app.internal.database import CLIENT, CONFIG, DB_NAME, DB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to DB
    app.mongodb_client = CLIENT
    app.database = DB

    try:
        CLIENT.admin.command("ping")
        print(f"Connected to staging DB ({DB_NAME}) successfully.")
    except Exception as e:
        print(e)

    yield

    # Shutdown connection
    CLIENT.close()
    print(f"Disconnected from staging DB ({DB_NAME}) successfully.")


app = FastAPI(
    title="Elevatus Technical Assignment",
    description="Technical Assignment by Elevatus for a Python Developer Role",
    lifespan=lifespan,
)

app.include_router(router)