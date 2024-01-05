from fastapi import APIRouter, FastAPI, Request, Response, status
from fastapi.routing import APIRoute


router = APIRouter()


@router.get("/health", response_description="Health Check", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "ok"}