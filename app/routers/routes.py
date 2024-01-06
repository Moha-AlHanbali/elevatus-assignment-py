"""
This module contains the API routes.

It defines routes for health check and provides functionality to detect the user and candidate context based on the production environment.
"""

from typing import List
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Header,
    Query,
    Request,
    HTTPException,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from app.internal.models import User, Candidate
from pymongo.errors import DuplicateKeyError

from app.internal.database import (
    USERS,
    CANDIDATES,
    TEST_USERS,
    TEST_CANDIDATES,
    PRODUCTION,
)


router = APIRouter()


def detect_user_context():
    """
    Detects the user context based on the production environment.

    Returns:
    - USERS collection for production.
    - TEST_USERS collection for testing.
    """
    if PRODUCTION == "true":
        return USERS
    else:
        return TEST_USERS


def detect_candidate_context():
    """
    Detects the candidate context based on the production environment.

    Returns:
    - CANDIDATES collection for production.
    - TEST_CANDIDATES collection for testing.
    """
    if PRODUCTION == "true":
        return CANDIDATES
    else:
        return TEST_CANDIDATES


def get_user_email(Authorization_Email: str = Header(...)):
    """
    Helper function to get the user's email from the Authorization header.

    Args:
    - Authorization_Email: Header containing the user's email.

    Returns:
    - User's email.
    """
    return Authorization_Email


@router.get(
    "/health", response_description="Health Check", status_code=status.HTTP_200_OK
)
def health_check():
    """
    Endpoint for performing a health check.

    Returns:
    - JSON response indicating the status as "ok".
    """
    return {"status": "ok"}


@router.post(
    "/user",
    response_description="Create a user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
def create_user(request: Request, user: User = Body(...)):
    """
    Endpoint for creating a user.

    Args:
    - request: FastAPI request object.
    - user: User model for the new user.

    Returns:
    - JSON response containing the created user.
    """
    try:
        user_collection = detect_user_context()

        existing_emails = [
            entry["email"] for entry in user_collection.find({}, {"email": 1})
        ]
        if user.email in existing_emails:
            return JSONResponse(
                content={"detail": "Email must be unique"}, status_code=400
            )

        user_dict = jsonable_encoder(user)

        new_user = request.app.database["user"].insert_one(user_dict)
        created_user = request.app.database["user"].find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user
    except DuplicateKeyError:
        return JSONResponse(content={"detail": "Email must be unique"}, status_code=400)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/candidate",
    response_description="Create a candidate",
    status_code=status.HTTP_201_CREATED,
    response_model=Candidate,
)
def create_candidate(
    request: Request, candidate: Candidate, user_email: str = Depends(get_user_email)
):
    """
    Endpoint for creating a candidate.

    Args:
    - request: FastAPI request object.
    - candidate: Candidate model for the new candidate.
    - user_email: User's email obtained from the Authorization header.

    Returns:
    - JSON response containing the created candidate.
    """
    user_collection = detect_user_context()
    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        candidate_collection = detect_candidate_context()
        existing_emails = [
            entry["email"] for entry in candidate_collection.find({}, {"email": 1})
        ]
        if candidate.email in existing_emails:
            raise DuplicateKeyError("Email must be unique")

        candidate_dict = jsonable_encoder(candidate)
        new_candidate = candidate_collection.insert_one(candidate_dict)
        created_candidate = candidate_collection.find_one(
            {"_id": new_candidate.inserted_id}
        )
        return created_candidate
    except DuplicateKeyError:
        return JSONResponse(
            content={"detail": "Email must be unique"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get(
    "/candidate/{candidate_id}",
    response_description="Get a candidate by ID",
    status_code=status.HTTP_200_OK,
    response_model=Candidate,
)
def get_candidate(
    request: Request, candidate_id: str, user_email: str = Depends(get_user_email)
):
    """
    Endpoint for retrieving a candidate by ID.

    Args:
    - request: FastAPI request object.
    - candidate_id: ID of the candidate to be retrieved.
    - user_email: User's email obtained from the Authorization header.

    Returns:
    - JSON response containing the retrieved candidate.
    """
    user_collection = detect_user_context()
    candidate_collection = detect_candidate_context()

    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    candidate = candidate_collection.find_one({"_id": candidate_id})
    if candidate:
        return candidate
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )


@router.put(
    "/candidate/{candidate_id}",
    response_description="Update a candidate by ID",
    status_code=status.HTTP_200_OK,
    response_model=Candidate,
)
def update_candidate(
    request: Request,
    candidate_id: str,
    candidate: Candidate,
    user_email: str = Depends(get_user_email),
):
    """
    Endpoint for updating a candidate by ID.

    Args:
    - request: FastAPI request object.
    - candidate_id: ID of the candidate to be updated.
    - candidate: Updated Candidate model.
    - user_email: User's email obtained from the Authorization header.

    Returns:
    - JSON response containing the updated candidate.
    """
    user_collection = detect_user_context()
    candidate_collection = detect_candidate_context()

    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    update_data = {
        key: value for key, value in jsonable_encoder(candidate).items() if key != "_id"
    }
    updated_candidate = candidate_collection.find_one_and_update(
        {"_id": candidate_id},
        {"$set": update_data},
        return_document=True,
    )
    if updated_candidate:
        return updated_candidate
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )


@router.delete(
    "/candidate/{candidate_id}",
    response_description="Delete a candidate by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_candidate(
    request: Request, candidate_id: str, user_email: str = Depends(get_user_email)
):
    """
    Endpoint for deleting a candidate by ID.

    Args:
    - request: FastAPI request object.
    - candidate_id: ID of the candidate to be deleted.
    - user_email: User's email obtained from the Authorization header.

    Returns:
    - JSON response indicating successful deletion or not found.
    """
    user_collection = detect_user_context()
    candidate_collection = detect_candidate_context()

    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = candidate_collection.delete_one({"_id": candidate_id})
    if result.deleted_count == 1:
        return JSONResponse(
            content={"detail": "Candidate deleted successfully"},
            status_code=status.HTTP_204_NO_CONTENT,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )


@router.get(
    "/all-candidates",
    response_description="Get all candidates",
    response_model=List[Candidate],
)
def get_all_candidates(
    request: Request,
    user_email: str = Depends(get_user_email),
    _id: str = Query(None, title="UUID", description="Filter by UUID"),
    first_name: str = Query(
        None, title="First Name", description="Filter by first name"
    ),
    last_name: str = Query(None, title="Last Name", description="Filter by last name"),
    email: str = Query(None, title="Email", description="Filter by email"),
    career_level: str = Query(
        None, title="Career Level", description="Filter by career level"
    ),
    job_major: str = Query(None, title="Job Major", description="Filter by job major"),
    years_of_experience: int = Query(
        None, title="Years of Experience", description="Filter by years of experience"
    ),
    degree_type: str = Query(
        None, title="Degree Type", description="Filter by degree type"
    ),
    skills: List[str] = Query(None, title="Skills", description="Filter by skills"),
    nationality: str = Query(
        None, title="Nationality", description="Filter by nationality"
    ),
    city: str = Query(None, title="City", description="Filter by city"),
    salary: float = Query(None, title="Salary", description="Filter by salary"),
    gender: List[str] = Query(None, title="Gender", description="Filter by gender"),
    keywords: str = Query(
        None, title="Keywords", description="Global search using keywords"
    ),
):
    """
    Endpoint for retrieving all candidates with optional filters.

    Args:
    - request: FastAPI request object.
    - user_email: User's email obtained from the Authorization header.
    - _id: Filter by candidate UUID.
    - first_name: Filter by candidate first name.
    - last_name: Filter by candidate last name.
    - email: Filter by candidate email.
    - career_level: Filter by candidate career level.
    - job_major: Filter by candidate job major.
    - years_of_experience: Filter by candidate years of experience.
    - degree_type: Filter by candidate degree type.
    - skills: Filter by candidate skills.
    - nationality: Filter by candidate nationality.
    - city: Filter by candidate city.
    - salary: Filter by candidate salary.
    - gender: Filter by candidate gender.
    - keywords: Global search using keywords.

    Returns:
    - List of candidates matching the specified filters.
    """
    user_collection = detect_user_context()
    candidate_collection = detect_candidate_context()

    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    filters = {}
    # Add filters for each field
    if _id:
        filters["_id"] = _id
    if first_name:
        filters["first_name"] = first_name
    if last_name:
        filters["last_name"] = last_name
    if email:
        filters["email"] = email
    if career_level:
        filters["career_level"] = career_level
    if job_major:
        filters["job_major"] = job_major
    if years_of_experience is not None:
        filters["years_of_experience"] = years_of_experience
    if degree_type:
        filters["degree_type"] = degree_type
    if skills:
        filters["skills"] = {"$all": skills}
    if nationality:
        filters["nationality"] = nationality
    if city:
        filters["city"] = city
    if salary is not None:
        filters["salary"] = salary
    if gender:
        filters["gender"] = gender

    # Add global search using keywords
    if keywords:
        global_search_filters = {
            "$or": [
                {"_id": {"$regex": keywords, "$options": "i"}},
                {"first_name": {"$regex": keywords, "$options": "i"}},
                {"last_name": {"$regex": keywords, "$options": "i"}},
                {"email": {"$regex": keywords, "$options": "i"}},
                {"career_level": {"$regex": keywords, "$options": "i"}},
                {"job_major": {"$regex": keywords, "$options": "i"}},
                {"years_of_experience": {"$regex": str(keywords), "$options": "i"}},
                {"degree_type": {"$regex": keywords, "$options": "i"}},
                {"nationality": {"$regex": keywords, "$options": "i"}},
                {"city": {"$regex": keywords, "$options": "i"}},
                {"skills": {"$in": [keywords]}},
                {"gender": {"$regex": keywords, "$options": "i"}},
                {"salary": {"$regex": str(keywords), "$options": "i"}},
            ]
        }
        filters["$or"] = global_search_filters["$or"]

    result = candidate_collection.find(filters)
    return list(result)


@router.get("/generate-report")
async def generate_report(
    request: Request,
    page: int = Query(1, gt=0, description="Page number for pagination"),
    page_size: int = Query(10, gt=0, le=100, description="Items per page"),
    user_email: str = Depends(get_user_email)
):
    """
    Endpoint for generating a report of all candidates in CSV format.

    Args:
    - request: FastAPI request object.
    - page: Page number for pagination (default: 1).
    - page_size: Items per page (default: 10, max: 100).

    Returns:
    - StreamingResponse: CSV file containing candidate information.
    """

    user_collection = detect_user_context()
    candidate_collection = detect_candidate_context()

    user = user_collection.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Calculate skip and limit based on pagination parameters
    skip = (page - 1) * page_size
    limit = page_size

    # Fetch candidates based on pagination
    candidates = list(candidate_collection.find().skip(skip).limit(limit))

    header = Candidate.model_json_schema()["properties"].keys()

    def generate_csv():
        yield ",".join(header) + "\n"

        for candidate in candidates:
            candidate_info = [str(candidate.get(field, "")) for field in header]
            yield ",".join(candidate_info) + "\n"

    response = StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=candidates_report.csv"},
    )

    return response