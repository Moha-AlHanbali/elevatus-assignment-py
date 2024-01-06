"""
This module is the entry point to the assignment project.

It initializes a FastAPI instance with database connection setup and checks for the production environment.
"""

import logging
from fastapi import FastAPI
from app.routers.routes import router
from contextlib import asynccontextmanager

from app.internal.settings import CLIENT, DB_NAME, DB, PRODUCTION

# Just to silence this warning mentioned here: https://github.com/pyca/bcrypt/issues/684
logging.getLogger('passlib').setLevel(logging.ERROR)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager to manage the lifespan of the FastAPI application.
    Connects to the production database, performs a ping test, and disconnects on exit.

    :param app: FastAPI application instance.
    """
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