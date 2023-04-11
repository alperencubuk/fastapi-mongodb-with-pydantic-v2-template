from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr

from source.core.database import PyObjectId


async def check_email(
    db: AsyncIOMotorDatabase, email: EmailStr, boilerplate_id: PyObjectId = None
) -> bool:
    if boilerplate := await db["boilerplate"].find_one({"email": email}):
        if not boilerplate_id or boilerplate.get("_id") != boilerplate_id:
            return False
    return True
