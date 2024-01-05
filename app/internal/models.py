"This module contains the DB models"

from pydantic import BaseModel, Field, EmailStr
from uuid import uuid4


class User(BaseModel):
    first_name: str 
    last_name: str 
    email: EmailStr 
    uuid: str = Field(
        default_factory=lambda: str(uuid4()),
        alias="_id",
        description="User's UUID",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uuid = str(uuid4())

    class ConfigDict:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "first_name": "Some First Name",
                "last_name": "Some Last Name",
                "email": "somemail@domain.com",
            }
        }
