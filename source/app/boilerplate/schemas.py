from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic_mongo import ObjectIdField

from source.app.boilerplate.enums import Order, Sort
from source.core.schemas import CreateModel, PageModel, ResponseModel, UpdateModel


class BoilerplateRequest(BaseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None


class BoilerplateCreate(CreateModel, BoilerplateRequest):
    pass


class BoilerplateResponse(ResponseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    create_date: datetime
    update_date: datetime


class BoilerplateApiResponse(BoilerplateResponse):
    id: str


class BoilerplateUpdateRequest(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class BoilerplateUpdate(UpdateModel, BoilerplateUpdateRequest):
    pass


class BoilerplatePage(PageModel):
    boilerplate: list[BoilerplateApiResponse]


class BoilerplatePagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=0)
    sort: Sort = Sort.ID
    order: Order = Order.ASC


class BoilerplateId(BaseModel):
    boilerplate_id: ObjectIdField
