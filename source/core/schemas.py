from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from source.core.database import PyObjectId


class CreateModel(BaseModel):
    create_date: datetime = Field(default_factory=datetime.utcnow)
    update_date: datetime | None = None

    @model_validator(mode="after")
    def update_date_validator(self) -> "CreateModel":
        self.update_date = self.create_date
        return self


class UpdateModel(BaseModel):
    update_date: datetime = Field(default_factory=datetime.utcnow)


class ResponseModel(BaseModel):
    id: PyObjectId = Field(alias="_id")


class PageModel(BaseModel):
    page: int
    size: int
    total: int
    pages: int


class ExceptionModel(BaseModel):
    detail: str


class HealthModel(BaseModel):
    api: bool
    database: bool
