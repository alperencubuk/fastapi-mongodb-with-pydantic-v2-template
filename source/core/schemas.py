from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, root_validator

from source.core.database import PyObjectId


class CreateModel(BaseModel):
    create_date: datetime = Field(default_factory=datetime.utcnow)
    update_date: datetime = None

    @root_validator
    def update_date_validator(cls, values) -> dict:
        values["update_date"] = values["create_date"]
        return values


class UpdateModel(BaseModel):
    update_date: datetime = Field(default_factory=datetime.utcnow)


class ResponseModel(BaseModel):
    id: PyObjectId = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class PageModel(BaseModel):
    page: int
    size: int
    total: int
    pages: int

    class Config:
        json_encoders = {ObjectId: str}


class ExceptionModel(BaseModel):
    detail: str


class HealthModel(BaseModel):
    api: bool
    database: bool
