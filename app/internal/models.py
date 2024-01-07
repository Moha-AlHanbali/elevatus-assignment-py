"""
This module contains the DB models.
"""

import datetime
from datetime import timedelta
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from typing import List, Literal
from uuid import uuid4
from app.internal.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt


# Set Hash algorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """
    Model for representing a user in the database.

    Attributes:
    - uuid: User's UUID.
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    - hashed_password: Hashed password.

    ConfigDict:
    - alias: Alias for the "_id" field.
    - json_extra: Additional JSON schema information, including an example.
    """
    uuid: str = Field(
        # Auto generated on User creation
        default_factory=lambda: str(uuid4()),
        alias="_id",
        description="User's UUID",
    )
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: EmailStr = Field(..., description="User's email address")
    hashed_password: str = Field(..., alias="password",description="Hashed password")

    class ConfigDict:
        alias = {"uuid": "_id"}
        json_extra = {
            "example": {
                "first_name": "Some First Name",
                "last_name": "Some Last Name",
                "email": "somemail@domain.com",
            }
        }
        exclude = {"hashed_password"}
    
    def set_password(self, password: str):
        """
        Hash and set the user's password.
        """
        self.hashed_password = pwd_context.hash(password)

class Auth(BaseModel):
    email: str
    password: str

    @staticmethod
    def create_access_token(data: dict):
        # Set expiration time
        expires = datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # Add it to the JWT Data dict
        to_encode = {"exp": expires, **data}
        # Encode the JWT
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def get_password(self, password: str, hashed_password: str):
        """
        Verify that provided password is indeed the user's hashed password.
        """
        return pwd_context.verify(password, hashed_password)

class Candidate(BaseModel):
    """
    Model for representing a candidate in the database.

    Attributes:
    - uuid: Candidate's UUID.
    - first_name: Candidate's first name.
    - last_name: Candidate's last name.
    - email: Candidate's email address.
    - career_level: Candidate's career level.
    - job_major: Candidate's job major.
    - years_of_experience: Candidate's years of experience.
    - degree_type: Candidate's degree type.
    - skills: List of candidate's skills.
    - nationality: Candidate's nationality.
    - city: Candidate's city.
    - salary: Candidate's salary.
    - gender: Candidate's gender.

    ConfigDict:
    - populate_by_name: Enables populating the model from dictionary keys.
    - json_schema_extra: Additional JSON schema information, including an example.
    """

    uuid: str = Field(
        default_factory=lambda: str(uuid4()),
        alias="_id",
        description="Candidate's UUID",
    )
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
