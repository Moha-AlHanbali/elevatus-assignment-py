"This module contains thr API routes"

from typing import List
from fastapi import APIRouter, Body, Query, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.internal.models import User, Candidate
from pymongo.errors import DuplicateKeyError
from bson.regex import Regex

from app.internal.database import USERS, CANDIDATES


router = APIRouter()


@router.get(
    "/health", response_description="Health Check", status_code=status.HTTP_200_OK
)
def health_check():
    return {"status": "ok"}


@router.post(
    "/user",
    response_description="Create a user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
def create_user(request: Request, user: User = Body(...)):
    try:
        existing_emails = [entry["email"] for entry in USERS.find({}, {"email": 1})]
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
def create_candidate(candidate: Candidate):
    try:
        existing_emails = [
            entry["email"] for entry in CANDIDATES.find({}, {"email": 1})
        ]
        if candidate.email in existing_emails:
            raise DuplicateKeyError("Email must be unique")

        candidate_dict = jsonable_encoder(candidate)
        new_candidate = CANDIDATES.insert_one(candidate_dict)
        created_candidate = CANDIDATES.find_one({"_id": new_candidate.inserted_id})
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
def get_candidate(candidate_id: str):
    candidate = CANDIDATES.find_one({"_id": candidate_id})
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
def update_candidate(candidate_id: str, candidate: Candidate):
    update_data = {
        key: value for key, value in jsonable_encoder(candidate).items() if key != "_id"
    }
    updated_candidate = CANDIDATES.find_one_and_update(
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
def delete_candidate(candidate_id: str):
    result = CANDIDATES.delete_one({"_id": candidate_id})
    if result.deleted_count == 1:
        return JSONResponse(
            content={"detail": "Candidate deleted successfully"},
            status_code=status.HTTP_204_NO_CONTENT,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )


# Assume CANDIDATES is the collection of candidates

@router.get("/all-candidates", response_description="Get all candidates", response_model=List[Candidate])
def get_all_candidates(
    _id:  str = Query(None, title="UUID", description="Filter by UUID"),
    first_name: str = Query(None, title="First Name", description="Filter by first name"),
    last_name: str = Query(None, title="Last Name", description="Filter by last name"),
    email: str = Query(None, title="Email", description="Filter by email"),
    career_level: str = Query(None, title="Career Level", description="Filter by career level"),
    job_major: str = Query(None, title="Job Major", description="Filter by job major"),
    years_of_experience: int = Query(None, title="Years of Experience", description="Filter by years of experience"),
    degree_type: str = Query(None, title="Degree Type", description="Filter by degree type"),
    skills: List[str] = Query(None, title="Skills", description="Filter by skills"),
    nationality: str = Query(None, title="Nationality", description="Filter by nationality"),
    city: str = Query(None, title="City", description="Filter by city"),
    salary: float = Query(None, title="Salary", description="Filter by salary"),
    gender: List[str] = Query(None, title="Gender", description="Filter by gender"),
    keywords: str = Query(None, title="Keywords", description="Global search using keywords"),
):
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
                # Add more fields for global search
            ]
        }
        filters["$or"] = global_search_filters["$or"]

    result = CANDIDATES.find(filters)
    return list(result)