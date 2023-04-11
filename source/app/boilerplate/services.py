from math import ceil

from motor.motor_asyncio import AsyncIOMotorDatabase

from source.app.boilerplate.enums import Order, Sort
from source.app.boilerplate.schemas import (
    BoilerplateCreate,
    BoilerplatePage,
    BoilerplateRequest,
    BoilerplateResponse,
    BoilerplateUpdate,
    BoilerplateUpdateRequest,
)
from source.app.boilerplate.utils import check_email
from source.core.database import PyObjectId


async def get_boilerplate(
    boilerplate_id: PyObjectId, db: AsyncIOMotorDatabase
) -> dict | None:
    if boilerplate := await db["boilerplate"].find_one({"_id": boilerplate_id}):
        return BoilerplateResponse(**boilerplate).dict()


async def list_boilerplate(
    page: int, size: int, sort: Sort, order: Order, db: AsyncIOMotorDatabase
) -> BoilerplatePage | None:
    if sort == Sort.ID.value:
        sort = "_id"
    order = 1 if order == Order.ASC.value else -1
    boilerplate_list = (
        await db["boilerplate"]
        .find()
        .sort(sort, order)
        .skip((page - 1) * size)
        .limit(size)
        .to_list(None)
    )

    boilerplate_list = [
        BoilerplateResponse(**boilerplate_item).dict()
        for boilerplate_item in boilerplate_list
    ]

    total = await db["boilerplate"].estimated_document_count()

    return BoilerplatePage(
        boilerplate=boilerplate_list,
        page=page,
        size=size,
        total=total,
        pages=(ceil(total / size) if size else 1),
    )


async def create_boilerplate(
    boilerplate: BoilerplateRequest, db: AsyncIOMotorDatabase
) -> dict | None:
    if await check_email(email=boilerplate.email, db=db):
        boilerplate = BoilerplateCreate(**boilerplate.dict())
        new_boilerplate = await db["boilerplate"].insert_one(boilerplate.dict())
        created_boilerplate = await db["boilerplate"].find_one(
            {"_id": new_boilerplate.inserted_id}
        )
        return BoilerplateResponse(**created_boilerplate).dict()


async def update_boilerplate(
    boilerplate_id: PyObjectId,
    boilerplate: BoilerplateUpdateRequest,
    db: AsyncIOMotorDatabase,
) -> dict | None:
    if await check_email(email=boilerplate.email, db=db):
        boilerplate = BoilerplateUpdate(**boilerplate.dict())
        fields_to_update = {
            k: v for k, v in boilerplate.dict().items() if v is not None
        }
        if updated_boilerplate := await db["boilerplate"].find_one_and_update(
            {"_id": boilerplate_id}, {"$set": fields_to_update}, return_document=True
        ):
            return BoilerplateResponse(**updated_boilerplate).dict()


async def delete_boilerplate(
    boilerplate_id: PyObjectId, db: AsyncIOMotorDatabase
) -> None:
    delete = await db["boilerplate"].delete_one({"_id": boilerplate_id})
    return delete.deleted_count
