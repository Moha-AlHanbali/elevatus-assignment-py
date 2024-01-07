"""
This module contains unit tests for the application.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.internal.settings import TEST_CLIENT, TEST_DB, TEST_DB_NAME, PRODUCTION
from app.routers.routes import router


app = FastAPI()
app.include_router(router)

candidate_test_id = {"value": ""}
access_token = {"value": ""}
auth_headers = {"Authorization": ""}
invalid_auth_headers = {"Authorization": f"Bearer {"SOME_INVALID_VALUE"}"}

@pytest.fixture
def test_app():
    with TestClient(app) as client:
        if PRODUCTION != "false":
            raise Exception("PLEASE DISABLE PRODUCTION ENVIRONMENT.")
        app.mongodb_client = TEST_CLIENT
        app.database = TEST_DB

        print(f"Connected to testing DB ({TEST_DB_NAME}) successfully.")

        TEST_USERS = TEST_DB["user"]
        TEST_CANDIDATES = TEST_DB["candidate"]

        TEST_USERS.create_index([("email", 1)], unique=True)
        TEST_CANDIDATES.create_index([("email", 1)], unique=True)
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
            "first_name": "application",
            "last_name": "user",
            "email": "useremail@example.com",
            "password": "testingPassword"

        },
    )
    assert response.status_code == 201


def test_create_user_duplicate_email(test_app):
    # First, create a user with a unique email
    response = test_app.post(
        "/user",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "strongPassword"
        },
    )
    assert response.status_code == 201

    # Attempt to create a user with the same email
    response = test_app.post(
        "/user",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "superstrongPassword"
        },
    )
    assert response.status_code == 400
    assert "Email must be unique" in response.json()["detail"]



def test_generate_token_valid_credentials(test_app):
    """
    Test the /token endpoint with valid user credentials.

    This test case ensures that the endpoint returns a valid JWT token when provided with correct credentials.

    Returns:
    - None
    """

    # Define valid user credentials for testing
    valid_credentials = {
        "email": "useremail@example.com",
        "password": "testingPassword"
    }

    # Send a POST request to the /token endpoint with valid credentials
    response = test_app.post("/token", json = valid_credentials)

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert that the response contains the expected keys
    assert "access_token" in response.json()
    assert "token_type" in response.json()

    access_token["value"] = response.json()["access_token"]
    auth_headers["Authorization"] = f"Bearer {access_token["value"]}"

def test_generate_token_invalid_credentials(test_app):
    """
    Test the /token endpoint with invalid user credentials.

    This test case ensures that the endpoint returns a 401 UNAUTHORIZED status code when provided with incorrect credentials.

    Returns:
    - None
    """

    # Define invalid user credentials for testing
    invalid_credentials = {
        "email": "nonexistent@example.com",
        "password": "incorrectpassword"
    }

    # Send a POST request to the /token endpoint with invalid credentials
    response = test_app.post("/token", json = invalid_credentials)

    # Assert that the response status code is 401 UNAUTHORIZED
    assert response.status_code == 401


def test_create_candidate(test_app):
    candidate_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "career_level": "Senior",
        "job_major": "Computer Science",
        "years_of_experience": 3,
        "degree_type": "Bachelor",
        "skills": ["Python", "RUBY", "Java"],
        "nationality": "US",
        "city": "NY",
        "salary": 2500000.0,
        "gender": "Male",
    }

    # Test with invalid authorization email
    response = test_app.post(
        "/candidate", json=candidate_data, headers=invalid_auth_headers
    )
    assert response.status_code == 401

    # Test with valid authorization email
    response = test_app.post(
        "/candidate", json=candidate_data, headers=auth_headers
    )
    print(response.json())
    print(auth_headers)
    candidate_test_id["value"] = response.json()["_id"]

    assert response.status_code == 201
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "email" in response.json()


def test_get_candidate(test_app):
    assert candidate_test_id["value"] is not None

    # Test with invalid authorization email
    response = test_app.get(
        f"/candidate/{candidate_test_id['value']}", headers=invalid_auth_headers
    )
    assert response.status_code == 401

    # Test with valid authorization email
    response = test_app.get(
        f"/candidate/{candidate_test_id['value']}", headers=auth_headers
    )
    assert response.status_code == 200
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "email" in response.json()


def test_update_candidate(test_app):
    candidate_data = {
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
        "gender": "Male",
    }

    # Test with invalid authorization email
    response = test_app.put(
        f"/candidate/{candidate_test_id['value']}",
        json=candidate_data,
        headers=invalid_auth_headers,
    )
    assert response.status_code == 401

    # Test with valid authorization email
    response = test_app.put(
        f"/candidate/{candidate_test_id['value']}",
        json=candidate_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert "first_name" in response.json()
    assert response.json()["first_name"] == "Mark"
    assert "last_name" in response.json()
    assert response.json()["last_name"] == "Smith"
    assert "email" in response.json()
    assert response.json()["email"] == "mark.doe@example.com"


def test_delete_candidate(test_app):

    # Test with invalid authorization email
    response = test_app.delete(
        f"/candidate/{candidate_test_id['value']}", headers=invalid_auth_headers
    )
    assert response.status_code == 401

    # Test with valid authorization email
    response = test_app.delete(
        f"/candidate/{candidate_test_id['value']}", headers=auth_headers
    )
    assert response.status_code == 204


def test_get_all_candidates(test_app):
    # Create test candidates
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
        headers=auth_headers,
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
            "nationality": "US",
            "city": "SF",
            "salary": 80000.0,
            "gender": "Female",
        },
        headers=auth_headers,
    )

    # Test global search with keywords (invalid authorization email)
    response = test_app.get(
        "/all-candidates?keywords=John", headers=invalid_auth_headers
    )
    assert response.status_code == 401

    # Test global search with keywords (valid authorization email)
    response = test_app.get(
        "/all-candidates?keywords=John", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["first_name"] == "John"

    # Test regular filters
    response = test_app.get(
        "/all-candidates?career_level=Senior&city=NY", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["first_name"] == "John"

    # Test global search with keywords and regular filters
    response = test_app.get(
        "/all-candidates?keywords=Doe&city=SF", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["first_name"] == "Jane"

    # Test when no candidates match the criteria
    response = test_app.get(
        "/all-candidates?keywords=InvalidName", headers=auth_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 0

    # Test with query string
    query_string = """first_name=Jane&last_name=Doe&email=jane.doe@example.com&career_level=Junior&job_major=Computer%20Information%20Systems&years_of_experience=2&degree_type=Master&nationality=US&city=SF"""

    response = test_app.get(
        f"/all-candidates?{query_string}", headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()[0]["first_name"] == "Jane"


def test_generate_report(test_app):

    # Create test candidates
    test_candidates = [
        {
            "first_name": "csvJohn",
            "last_name": "Doe",
            "email": "csvjohn.doe@example.com",
            "career_level": "Senior",
            "job_major": "Computer Science",
            "years_of_experience": 3,
            "degree_type": "Bachelor",
            "skills": ["Python", "RUBY", "Java"],
            "nationality": "US",
            "city": "NY",
            "salary": 2500000.0,
            "gender": "Male",
        },
        {
            "first_name": "csvJane",
            "last_name": "Doe",
            "email": "csvjane.doe@example.com",
            "career_level": "Junior",
            "job_major": "Accounting",
            "years_of_experience": 1,
            "degree_type": "Masters",
            "skills": ["Javascript"],
            "nationality": "US",
            "city": "NY",
            "salary": 800000.0,
            "gender": "Female",
        },
    ]

    # Create test candidates in the database
    for candidate_data in test_candidates:
        test_app.post("/candidate", json=candidate_data, headers=auth_headers)

    response = test_app.get("/generate-report", headers=invalid_auth_headers)
    assert response.status_code == 401


    # Make a request to generate the report
    response = test_app.get("/generate-report", headers=auth_headers)

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response headers
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert (
        response.headers["content-disposition"]
        == "attachment; filename=candidates_report.csv"
    )

    # Assert the content of the CSV file
    expected_headers = "_id,first_name,last_name,email,career_level,job_major,years_of_experience,degree_type,skills,nationality,city,salary,gender\n"
    assert response.text.startswith(expected_headers)

    # You can add additional assertions based on the expected content of the report


def test_cleanup(test_app):
    # Drop the user and candidate collections in the testing database
    app.database.drop_collection("user")
    app.database.drop_collection("candidate")
    test_app.close()
    print(f"Disconnected from testing DB ({TEST_DB_NAME}) successfully.")
