from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr
from pydantic_mongo import ObjectIdField


async def check_email(
    db: AsyncIOMotorDatabase,
    email: EmailStr,
    boilerplate_id: ObjectIdField | None = None,
) -> bool:
    if boilerplate := await db["boilerplate"].find_one({"email": email}):
        if not boilerplate_id or boilerplate.get("_id") != boilerplate_id:
            return False
    return True
