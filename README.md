# Elevatus Technical Assignment

This project is the implementation of the Elevatus Technical Assignment for a Python Developer Role.

## Table of Contents

- [Elevatus Technical Assignment](#elevatus-technical-assignment)
  - [Table of Contents](#table-of-contents)
  - [Keynotes About the Implementation](#keynotes-about-the-implementation)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Installing Locally](#installing-locally)
      - [Installing Containerized Version](#installing-containerized-version)
    - [Running the Application](#running-the-application)
    - [API Documentation](#api-documentation)
      - [Health Check](#health-check)
    - [Create User](#create-user)
      - [Request](#request)
        - [Request Body](#request-body)
      - [Response](#response)
      - [Error Responses](#error-responses)
        - [400 Bad Request](#400-bad-request)
        - [500 Internal Server Error](#500-internal-server-error)
      - [User Model](#user-model)
    - [Create Candidate](#create-candidate)
      - [Request](#request-1)
        - [Request Body](#request-body-1)
        - [Dependencies](#dependencies)
      - [Response](#response-1)
      - [Error Responses](#error-responses-1)
        - [400 Bad Request](#400-bad-request-1)
        - [401 Unauthorized](#401-unauthorized)
        - [500 Internal Server Error](#500-internal-server-error-1)
      - [Candidate Model](#candidate-model)
    - [Get Candidate by ID](#get-candidate-by-id)
      - [Request](#request-2)
        - [Dependencies](#dependencies-1)
      - [Response](#response-2)
      - [Error Responses](#error-responses-2)
        - [401 Unauthorized](#401-unauthorized-1)
        - [404 Not Found](#404-not-found)
      - [Candidate Model](#candidate-model-1)
    - [Update Candidate by ID](#update-candidate-by-id)
      - [Request](#request-3)
        - [Dependencies](#dependencies-2)
      - [Response](#response-3)
      - [Error Responses](#error-responses-3)
        - [401 Unauthorized](#401-unauthorized-2)
        - [404 Not Found](#404-not-found-1)
      - [Candidate Model](#candidate-model-2)
    - [Delete Candidate by ID](#delete-candidate-by-id)
      - [Request](#request-4)
        - [Dependencies](#dependencies-3)
      - [Response](#response-4)
      - [Error Responses](#error-responses-4)
        - [401 Unauthorized](#401-unauthorized-3)
        - [404 Not Found](#404-not-found-2)
    - [Get All Candidates](#get-all-candidates)
      - [Request](#request-5)
      - [Response](#response-5)
      - [Error Responses](#error-responses-5)
        - [401 Unauthorized](#401-unauthorized-4)
        - [400 Bad Request](#400-bad-request-2)
    - [Generate Report](#generate-report)
      - [Request](#request-6)
      - [Response](#response-6)
      - [Error Responses](#error-responses-6)
        - [401 Unauthorized](#401-unauthorized-5)
        - [400 Bad Request](#400-bad-request-3)
    - [Testing](#testing)
    - [Built With](#built-with)
    - [File Structure](#file-structure)
    - [Test Coverage](#test-coverage)

## Keynotes About the Implementation

1. `UUID` fields for both `user` and `candidate` collections are system-handled and auto generated, which are also used as the `ID` query parameter in the APIs.
2. `Email` field was set as a unique field in both collections as well (each separately).
3. The required authorization was handled by requesting the user email in `Authorization-Email` header (no authentication implemented).

## Getting Started

This project is a FastAPI-based web application. Follow the steps below to get started.

### Prerequisites

- Python 3.12
- MongoDB
- Docker and Docker Compose Plugin

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/elevatus-technical-assignment.git
    ```

2. Navigate to the project directory:

    ```bash
    cd elevatus-technical-assignment
    ```

3. Create `.env` file at the root directory level of the application and enter the required environment variables using `.env.sample` as a reference.

#### Installing Locally

- Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

or if you're using Poetry:

```bash
poetry install
```

#### Installing Containerized Version

- Run the command

```bash
sudo docker compose up
```

### Running the Application

To run the application, use the following command:

```bash
uvicorn app.main:app --reload
```

The application will be accessible at `http://localhost:8000`.

### API Documentation

The API provides various endpoints for managing users and candidates. Below are some of the key endpoints:

#### Health Check

URL: `/health`
Method: `GET`
Response:

```json
{"status": "ok"}
```

### Create User

Endpoint for creating a user.

- **URL:** `/user`
- **Method:** `POST`
- **Response Description:** Create a user
- **Status Code:** 201 Created
- **Response Model:** [User](#user-model)

#### Request

##### Request Body

- **Body:**
  - Type: JSON
  - Description: User model for the new user.
  - Example:

    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }
    ```

#### Response

- **Status Code:** 201 Created
- **Response Body:**
  - Type: JSON
  - Description: JSON response containing the created user.
  - Example:

    ```json
    {
      "_id": "generated_user_id",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }
    ```

#### Error Responses

##### 400 Bad Request

- **Response Body:**
  - Type: JSON
  - Description: Email must be unique.
  - Example:

    ```json
    {
      "detail": "Email must be unique"
    }
    ```

##### 500 Internal Server Error

- **Response Body:**
  - Type: JSON
  - Description: Internal server error.
  - Example:

    ```json
    {
      "detail": "Internal Server Error"
    }
    ```

#### User Model

```json
{
  "_id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string"
}
```

### Create Candidate

Endpoint for creating a candidate.

- **URL:** `/candidate`
- **Method:** `POST`
- **Response Description:** Create a candidate
- **Status Code:** 201 Created
- **Response Model:** [Candidate](#candidate-model)

#### Request

##### Request Body

- **Body:**
  - Type: JSON
  - Description: Candidate model for the new candidate.
  - Example:

    ```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "career_level": "Senior",
      "job_major": "Computer Science",
      "years_of_experience": 3,
      "degree_type": "Bachelor",
      "skills": ["Python", "JavaScript"],
      "nationality": "US",
      "city": "NY",
      "salary": 100000.0,
      "gender": "Male"
    }
    ```

##### Dependencies

- **Dependencies:**
  - Type: Header
  - Description: User's email obtained from the Authorization header.
  - Example:

    ```plaintext
    Authorization-Email: useremail@example.com
    ```

#### Response

- **Status Code:** 201 Created
- **Response Body:**
  - Type: JSON
  - Description: JSON response containing the created candidate.
  - Example:

    ```json
    {
      "_id": "generated_candidate_id",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "career_level": "Senior",
      "job_major": "Computer Science",
      "years_of_experience": 3,
      "degree_type": "Bachelor",
      "skills": ["Python", "JavaScript"],
      "nationality": "US",
      "city": "NY",
      "salary": 100000.0,
      "gender": "Male"
    }
    ```

#### Error Responses

##### 400 Bad Request

- **Response Body:**
  - Type: JSON
  - Description: Email must be unique.
  - Example:

    ```json
    {
      "detail": "Email must be unique"
    }
    ```

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:

    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 500 Internal Server Error

- **Response Body:**
  - Type: JSON
  - Description: Internal server error.
  - Example:

    ```json
    {
      "detail": "Internal Server Error"
    }
    ```

#### Candidate Model

```json
{
  "_id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "career_level": "string",
  "job_major": "string",
  "years_of_experience": 0,
  "degree_type": "string",
  "skills": ["string"],
  "nationality": "string",
  "city": "string",
  "salary": 0.0,
  "gender": "string"
}
```

### Get Candidate by ID

Endpoint for retrieving a candidate by ID.

- **URL:** `/candidate/{candidate_id}`
- **Method:** `GET`
- **Response Description:** Get a candidate by ID
- **Status Code:** 200 OK
- **Response Model:** [Candidate](#candidate-model)

#### Request

- **Parameters:**
  - `candidate_id` (Path Parameter)
    - Type: String
    - Description: ID of the candidate to be retrieved.
    - Example: `"generated_candidate_id"`

##### Dependencies

- **Dependencies:**
  - Type: Header
  - Description: User's email obtained from the Authorization header.
  - Example:

    ```plaintext
    Authorization-Email: useremail@example.com
    ```

#### Response

- **Status Code:** 200 OK
- **Response Body:**
  - Type: JSON
  - Description: JSON response containing the retrieved candidate.
  - Example:

    ```json
    {
      "_id": "generated_candidate_id",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "career_level": "Senior",
      "job_major": "Computer Science",
      "years_of_experience": 3,
      "degree_type": "Bachelor",
      "skills": ["Python", "JavaScript"],
      "nationality": "US",
      "city": "NY",
      "salary": 100000.0,
      "gender": "Male"
    }
    ```

#### Error Responses

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:

    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 404 Not Found

- **Response Body:**
  - Type: JSON
  - Description: Candidate not found.
  - Example:

    ```json
    {
      "detail": "Candidate not found"
    }
    ```

#### Candidate Model

```json
{
  "_id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "career_level": "string",
  "job_major": "string",
  "years_of_experience": 0,
  "degree_type": "string",
  "skills": ["string"],
  "nationality": "string",
  "city": "string",
  "salary": 0.0,
  "gender": "string"
}
```

### Update Candidate by ID

Endpoint for updating a candidate by ID.

- **URL:** `/candidate/{candidate_id}`
- **Method:** `PUT`
- **Response Description:** Update a candidate by ID
- **Status Code:** 200 OK
- **Response Model:** [Candidate](#candidate-model)

#### Request

- **Parameters:**
  - `candidate_id` (Path Parameter)
    - Type: String
    - Description: ID of the candidate to be updated.
    - Example: `"generated_candidate_id"`
  - `candidate` (Request Body)
    - Type: JSON
    - Description: Updated Candidate model.
    - Example:

      ```json
      {
        "first_name": "Updated John",
        "last_name": "Updated Doe",
        "email": "updated.john.doe@example.com",
        "career_level": "Senior",
        "job_major": "Computer Science",
        "years_of_experience": 3,
        "degree_type": "Bachelor",
        "skills": ["Python", "JavaScript"],
        "nationality": "US",
        "city": "NY",
        "salary": 100000.0,
        "gender": "Male"
      }
      ```

##### Dependencies

- **Dependencies:**
  - Type: Header
  - Description: User's email obtained from the Authorization header.
  - Example:

    ```plaintext
    Authorization-Email: useremail@example.com
    ```

#### Response

- **Status Code:** 200 OK
- **Response Body:**
  - Type: JSON
  - Description: JSON response containing the updated candidate.
  - Example:

    ```json
    {
      "_id": "generated_candidate_id",
      "first_name": "Updated John",
      "last_name": "Updated Doe",
      "email": "updated.john.doe@example.com",
      "career_level": "Senior",
      "job_major": "Computer Science",
      "years_of_experience": 3,
      "degree_type": "Bachelor",
      "skills": ["Python", "JavaScript"],
      "nationality": "US",
      "city": "NY",
      "salary": 100000.0,
      "gender": "Male"
    }
    ```

#### Error Responses

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:

    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 404 Not Found

- **Response Body:**
  - Type: JSON
  - Description: Candidate not found.
  - Example:
  
    ```json
    {
      "detail": "Candidate not found"
    }
    ```

#### Candidate Model

```json
{
  "_id": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "career_level": "string",
  "job_major": "string",
  "years_of_experience": 0,
  "degree_type": "string",
  "skills": ["string"],
  "nationality": "string",
  "city": "string",
  "salary": 0.0,
  "gender": "string"
}
```

### Delete Candidate by ID

Endpoint for deleting a candidate by ID.

- **URL:** `/candidate/{candidate_id}`
- **Method:** `DELETE`
- **Response Description:** Delete a candidate by ID
- **Status Code:** 204 No Content

#### Request

- **Parameters:**
  - `candidate_id` (Path Parameter)
    - Type: String
    - Description: ID of the candidate to be deleted.
    - Example: `"generated_candidate_id"`

##### Dependencies

- **Dependencies:**
  - Type: Header
  - Description: User's email obtained from the Authorization header.
  - Example:

    ```plaintext
    Authorization-Email: useremail@example.com
    ```

#### Response

- **Status Code:** 204 No Content
- **Response Body:**
  - Type: JSON
  - Description: JSON response indicating successful deletion or not found.
  - Example (Candidate found and deleted successfully):

    ```json
    {
      "detail": "Candidate deleted successfully"
    }
    ```

#### Error Responses

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:

    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 404 Not Found

- **Response Body:**
  - Type: JSON
  - Description: Candidate not found.
  - Example:

    ```json
    {
      "detail": "Candidate not found"
    }
    ```

### Get All Candidates

Endpoint for retrieving all candidates with optional filters.

- **URL:** `/all-candidates`
- **Method:** `GET`
- **Response Description:** Get all candidates
- **Response Model:** List of [Candidate](#candidate) models

#### Request

- **Parameters:**
  - `user_email` (Header Parameter)
    - Type: String
    - Description: User's email obtained from the Authorization header.
    - Example:

      ```plaintext
      Authorization-Email: useremail@example.com
      ```

  - `UUID` (Query Parameter)
    - Type: String
    - Title: UUID
    - Description: Filter by UUID.
    - Example: `"generated_candidate_id"`
  - `First Name` (Query Parameter)
    - Type: String
    - Title: First Name
    - Description: Filter by candidate first name.
    - Example: `"John"`
  - `Last Name` (Query Parameter)
    - Type: String
    - Title: Last Name
    - Description: Filter by candidate last name.
    - Example: `"Doe"`
  - `Email` (Query Parameter)
    - Type: String
    - Title: Email
    - Description: Filter by candidate email.
    - Example: `"john.doe@example.com"`
  - `Career Level` (Query Parameter)
    - Type: String
    - Title: Career Level
    - Description: Filter by candidate career level.
    - Example: `"Senior"`
  - `Job Major` (Query Parameter)
    - Type: String
    - Title: Job Major
    - Description: Filter by candidate job major.
    - Example: `"Computer Science"`
  - `Years of Experience` (Query Parameter)
    - Type: Integer
    - Title: Years of Experience
    - Description: Filter by candidate years of experience.
    - Example: `3`
  - `Degree Type` (Query Parameter)
    - Type: String
    - Title: Degree Type
    - Description: Filter by candidate degree type.
    - Example: `"Bachelor"`
  - `Skills` (Query Parameter)
    - Type: List of Strings
    - Title: Skills
    - Description: Filter by candidate skills.
    - Example: `["Python", "Java"]`
  - `Nationality` (Query Parameter)
    - Type: String
    - Title: Nationality
    - Description: Filter by candidate nationality.
    - Example: `"US"`
  - `City` (Query Parameter)
    - Type: String
    - Title: City
    - Description: Filter by candidate city.
    - Example: `"NY"`
  - `Salary` (Query Parameter)
    - Type: Float
    - Title: Salary
    - Description: Filter by candidate salary.
    - Example: `100000.0`
  - `Gender` (Query Parameter)
    - Type: List of Strings
    - Title: Gender
    - Description: Filter by candidate gender.
    - Example: `["Male", "Female"]`
  - `Keywords` (Query Parameter)
    - Type: String
    - Title: Keywords
    - Description: Global search using keywords.
    - Example: `"John Doe"`

#### Response

- **Status Code:** 200 OK
- **Response Body:**
  - Type: JSON
  - Description: List of [Candidate](#candidate) models matching the specified filters.
  - Example:

    ```json
    [
      {
        "_id": "generated_candidate_id",
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
        "gender": "Male"
      },
      {
        "_id": "generated_candidate_id_2",
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
        "gender": "Female"
      }
    ]
    ```

#### Error Responses

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:
  
    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 400 Bad Request

- **Response Body:**
  - Type: JSON
  - Description: Invalid request parameters or missing required parameters.
  - Example:

    ```json
    {
      "detail": "Invalid request parameters"
    }
    ```

### Generate Report

Endpoint for generating a report of all candidates in CSV format.

- **URL:** `/generate-report`
- **Method:** `GET`
- **Response Description:** StreamingResponse: CSV file containing candidate information.

#### Request

- **Parameters:**
  - `user_email` (Header Parameter)
    - Type: String
    - Description: User's email obtained from the Authorization header.
    - Example:

      ```plaintext
      Authorization-Email: useremail@example.com
      ```

  - `Page` (Query Parameter)
    - Type: Integer
    - Description: Page number for pagination (default: 1).
    - Example: `1`
  - `Page Size` (Query Parameter)
    - Type: Integer
    - Description: Items per page (default: 10, max: 100).
    - Example: `10`

#### Response

- **Status Code:** 200 OK
- **Response Body:**
  - Type: StreamingResponse
  - Description: CSV file containing candidate information.
  - Headers:
    - Content-Type: `text/csv; charset=utf-8`
    - Content-Disposition: `attachment; filename=candidates_report.csv`
  - Example:

    ```csv
    _id,first_name,last_name,email,career_level,job_major,years_of_experience,degree_type,skills,nationality,city,salary,gender
    generated_candidate_id,John,Doe,john.doe@example.com,Senior,Computer Science,3,Bachelor,"['Python', 'Java']",US,NY,100000.0,Male
    generated_candidate_id_2,Jane,Doe,jane.doe@example.com,Junior,Computer Information Systems,2,Master,"['JavaScript', 'SQL']",US,SF,80000.0,Female
    ```

#### Error Responses

##### 401 Unauthorized

- **Response Body:**
  - Type: JSON
  - Description: Unauthorized.
  - Example:
  
    ```json
    {
      "detail": "Unauthorized"
    }
    ```

##### 400 Bad Request

- **Response Body:**
  - Type: JSON
  - Description: Invalid request parameters or missing required parameters.
  - Example:
  
    ```json
    {
      "detail": "Invalid request parameters"
    }
    ```

### Testing

```bash
pytest
```

or to view test coverage:

```bash
coverage run -m pytest  
coverage report -m
```

### Built With

[FastAPI](https://fastapi.tiangolo.com) - The web framework used
[Pydantic](https://docs.pydantic.dev) - Used for data validation and settings management
[MongoDB](https://www.mongodb.com) - Database used

### File Structure

```bash
.
├── Dockerfile
├── LICENSE
├── README.md
├── __init__.py
├── app
│   ├── __init__.py
│   ├── internal
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── main.py
│   └── routers
│       ├── __init__.py
│       └── routes.py
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── requirements.txt
└── tests
    ├── __init__.py
    └── test_main.py
```

### Test Coverage

```md
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
app/internal/database.py      19      0   100%
app/internal/models.py        28      0   100%
app/routers/routes.py        146     18    88%
tests/test_main.py           120      1    99%
--------------------------------------------------------
TOTAL                        313     19    94%
```
