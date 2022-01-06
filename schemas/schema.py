from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime


class User(BaseModel):
    username: EmailStr
    company: str
    password: str


class UserRegister(BaseModel):

    username: EmailStr = Field(...)
    password: str = Field(..., title="Password", min_length=6)
    first_name: str = Field(..., title="User First Name", min_length=2, max_length=30)
    last_name: str = Field(..., title="User Last Name", min_length=2, max_length=30)
    company: Optional[str] = Field(
        ..., title="User Company Name", min_length=2, max_length=45
    )
    location: Optional[str] = Field(
        ..., title="User Location Country", min_length=2, max_length=45
    )

    class Config:
        schema_extra = {
            "example": {
                "username": "example@test.com",
                "password": "anyPassword1514",
                "first_name": "Charles",
                "last_name": "Carlson",
                "company": "Intel",
                "location": "China",
            }
        }


class UserStore(BaseModel):
    username: EmailStr
    password: str
    first_name: str
    last_name: str
    company: Optional[str]
    location: Optional[str]
    register_date: Optional[datetime]


from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class UserDisplay(BaseModel):
    _id: PydanticObjectId
    username: str
    first_name: str
    last_name: str
    company: Optional[str]
    location: Optional[str]
    register_date: Optional[datetime]


class Login(BaseModel):
    username: str
    password: str

    first_name: str
    last_name: str
    company: Optional[str]
    location: Optional[str]


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = Field(
        None, title="User First Name", min_length=2, max_length=30
    )
    last_name: Optional[str] = Field(
        None, title="User Last Name", min_length=2, max_length=30
    )
    company: Optional[str] = Field(
        None, title="User Company Name", min_length=2, max_length=45
    )
    location: Optional[str] = Field(
        None, title="Location Name", min_length=2, max_length=45
    )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Snow",
                "company": "Google",
                "location": "New York",
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class coursesCreation(BaseModel):
    title: str = Field(..., title="email user by the client to login", max_length=100)
    description: str = Field(None, title="Description of the product", max_length=300)
    youtube_video: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None


class coursesCreationDisplay(BaseModel):
    id: str
    title: str
    description: str
    youtube_video: Optional[HttpUrl]
    image_url: Optional[HttpUrl]
    Author: str
    created_at: datetime


class postSpecific(BaseModel):
    title: str
    description: str
    youtube_video: Optional[HttpUrl]
    image_url: Optional[HttpUrl]
    Author: str
    created_at: datetime
