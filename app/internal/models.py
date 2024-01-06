"This module contains the DB models"

from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from uuid import uuid4


class User(BaseModel):
    uuid: str = Field(
        default_factory=lambda: str(uuid4()),
        alias="_id",
        description="User's UUID",
    )
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address")

    class ConfigDict:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "first_name": "Some First Name",
                "last_name": "Some Last Name",
                "email": "somemail@domain.com",
            }
        }


class Candidate(BaseModel):

    uuid: str = Field( default_factory=lambda: str(uuid4()), alias="_id", description="Candidate's UUID")
    first_name: str = Field(..., description="Candidate's first name")
    last_name: str = Field(..., description="Candidate's last name")
    email: EmailStr = Field(..., description="Candidate's email address")
    career_level: str = Field(..., description="Candidate's career level")
    job_major: str = Field(..., description="Candidate's job major")
    years_of_experience: int = Field(..., description="Candidate's years of experience")
    degree_type: str = Field(..., description="Candidate's degree type")
    skills: List[str] = Field(..., description="List of candidate's skills")
    nationality: str = Field(..., description="Candidate's nationality")
    city: str = Field(..., description="Candidate's city")
    salary: float = Field(..., description="Candidate's salary")
    gender: Literal["Male", "Female", "Not Specified"] = Field(
        ..., description="Candidate's gender"
    )


    class ConfigDict:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "first_name": "Some",
                "last_name": "Name",
                "email": "somemail@domain.com",
                "career_level": "Senior",
                "job_major": "Computer Science",
                "years_of_experience": 3,
                "degree_type": "Bachelor",
                "skills": ["Python", "JavaScript"],
                "nationality": "JO",
                "city": "Amman",
                "salary": 100000.0,
                "gender": "Male",
            }
        }
