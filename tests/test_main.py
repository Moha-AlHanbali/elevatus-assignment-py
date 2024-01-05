from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.internal.database import CLIENT, DB_NAME, TEST_DB_PREFIX
from app.routers.routes import router

app = FastAPI()
app.include_router(router)

candidate_test_id = {"value": ""}


@pytest.fixture
def test_app():
    with TestClient(app) as client:
        app.mongodb_client = CLIENT
        app.database = CLIENT[TEST_DB_PREFIX + DB_NAME]
        app.database.drop_collection("user")
        app.database.drop_collection("candidate")
        USERS = CLIENT[TEST_DB_PREFIX + DB_NAME]["user"]
        USERS.create_index([("email", 1)], unique=True)
        CANDIDATES = CLIENT[TEST_DB_PREFIX + DB_NAME]["candidate"]
        CANDIDATES.create_index([("email", 1)], unique=True)
        yield client


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
        "/user",
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



def test_create_candidate(test_app):
    response = test_app.post(
        "/candidate",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "1john.doe@example.com",
            "career_level": "Senior",
            "job_major": "Computer Science",
            "years_of_experience": 3,
            "degree_type": "Bachelor",
            "skills": ["Python", "RUBY", "Java"],
            "nationality": "US",
            "city": "NY",
            "salary": 2500000.0,
            "gender": "Male"
        },
    )
    candidate_test_id["value"] = response.json()["_id"]

    assert response.status_code == 201
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "email" in response.json()

def test_get_candidate(test_app):
    assert candidate_test_id["value"] is not None
    response = test_app.get(f"/candidate/{candidate_test_id["value"]}")
    assert response.status_code == 200
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "email" in response.json()

def test_update_candidate(test_app):
    response = test_app.put(
        f"/candidate/{candidate_test_id["value"]}",
        json={
            "first_name": "Mark",
            "last_name": "Smith",
            "email": "mark.doe@example.com",
            "career_level": "Junior",
            "job_major": "Computer Science",
            "years_of_experience": 1,
            "degree_type": "Bachelor",
            "skills": ["Javascript"],
            "nationality": "US",
            "city": "CA",
            "salary": 600000,
            "gender": "Male"
        },
    )
    assert response.status_code == 200
    assert "first_name" in response.json()
    assert response.json()["first_name"] == "Mark"
    assert "last_name" in response.json()
    assert response.json()["last_name"] == "Smith"
    assert "email" in response.json()
    assert response.json()["email"] == "mark.doe@example.com"

def test_delete_candidate(test_app):
    response = test_app.delete(f"/candidate/{candidate_test_id["value"]}")
    assert response.status_code == 204



def test_get_all_candidates(test_app):
    # Create some test candidates
    test_app.post(
        "/candidate",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "career_level": "Senior",
            "job_major": "Computer Science",
            "years_of_experience": 3,
            "degree_type": "Bachelor",
            "skills": ["Python", "Java"],
            "nationality": "US",
            "city": "NY",
            "salary": 100000.0,
            "gender": "Male",
        },
    )
    test_app.post(
        "/candidate",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "career_level": "Junior",
            "job_major": "Computer Information Systems",
            "years_of_experience": 2,
            "degree_type": "Master",
            "skills": ["JavaScript", "SQL"],
            "nationality": "CA",
            "city": "SF",
            "salary": 80000.0,
            "gender": "Female",
        },
    )

    # Test global search with keywords
    response = test_app.get("/all-candidates?keywords=John")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "John"

    # Test regular filters
    response = test_app.get("/all-candidates?career_level=Senior&city=NY")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "John"

    # Test global search with keywords and regular filters
    response = test_app.get("/all-candidates?keywords=Doe&city=SF")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "Jane"

    # Test when no candidates match the criteria
    response = test_app.get("/all-candidates?keywords=InvalidName")
    assert response.status_code == 200
    assert len(response.json()) == 0
