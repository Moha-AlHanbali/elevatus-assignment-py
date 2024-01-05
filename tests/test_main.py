from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.internal.database import CLIENT, DB_NAME
from app.routers.routes import router

app = FastAPI()
app.include_router(router)



@pytest.fixture
def test_app():
    with TestClient(app) as client:
        app.mongodb_client = CLIENT
        app.database = CLIENT[DB_NAME + "test"]
        USERS = CLIENT[DB_NAME + "test"]["user"]
        USERS.create_index([("email", 1)], unique=True)
        yield client
        app.database.drop_collection("user")


def test_health_check(test_app):
    # Act
    response = test_app.get("/health")
    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user_unique_email(test_app):
    response = test_app.post(
        "/user",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        },
    )
    assert response.status_code == 201

def test_create_user_duplicate_email(test_app):
    # First, create a user with a unique email
    response = test_app.post(
        "/user/",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
    )
    assert response.status_code == 201

    # Attempt to create a user with the same email
    response = test_app.post(
        "/user",
        json={"first_name": "Jane", "last_name": "Doe", "email": "john.doe@example.com"},
    )
    assert response.status_code == 400
    assert "Email must be unique" in response.json()["detail"]