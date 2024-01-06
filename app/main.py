"This module is the entry point to the assignment project"

from fastapi import FastAPI
from app.routers.routes import router
from contextlib import asynccontextmanager

from app.internal.database import CLIENT, DB_NAME, DB, PRODUCTION


@asynccontextmanager
async def lifespan(app: FastAPI):
    if PRODUCTION != "true":
        raise Exception("PLEASE ENABLE PRODUCTION ENVIRONMENT.")
    # Connect to DB
    app.mongodb_client = CLIENT
    app.database = DB
    try:
        CLIENT.admin.command("ping")
        print(f"Connected to production DB ({DB_NAME}) successfully.")
    except Exception as e:
        print(e)

    yield

    # Shutdown connection
    CLIENT.close()
    print(f"Disconnected from production DB ({DB_NAME}) successfully.")


app = FastAPI(
    title="Elevatus Technical Assignment",
    description="Technical Assignment by Elevatus for a Python Developer Role",
    lifespan=lifespan,
)

app.include_router(router)