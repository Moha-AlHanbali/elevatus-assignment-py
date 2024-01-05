'This module contains thr API routes'

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.internal.models import User
from pymongo.errors import DuplicateKeyError

from app.internal.database import USERS


router = APIRouter()


@router.get(
    "/health", response_description="Health Check", status_code=status.HTTP_200_OK
)
def health_check():
    return {"status": "ok"}


@router.post("/user", response_description="Create a user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User = Body(...)):
    try:
        existing_emails = [entry["email"] for entry in USERS.find({}, {"email": 1})]
        if user.email in existing_emails:
            return JSONResponse(content={"detail": "Email must be unique"}, status_code=400)

        user_dict = jsonable_encoder(user)
        
        new_user = request.app.database["user"].insert_one(user_dict)
        created_user = request.app.database["user"].find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user
    except DuplicateKeyError:
        return JSONResponse(content={"detail": "Email must be unique"}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
