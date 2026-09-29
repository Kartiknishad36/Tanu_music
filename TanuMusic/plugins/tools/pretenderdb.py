from typing import Dict, List, Union
from config import MONGO_DB_URI
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

mongo = MongoCli(MONGO_DB_URI).Rankings
pretdb = mongo.pretender

async def is_pretender(chat_id: int, user_id: int) -> bool:
    data = await pretdb.find_one({"chat_id": chat_id, "user_id": user_id})
    return bool(data)

async def add_pretender(chat_id: int, user_id: int):
    await pretdb.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"chat_id": chat_id, "user_id": user_id}},
        upsert=True,
    )

async def remove_pretender(chat_id: int, user_id: int):
    await pretdb.delete_one({"chat_id": chat_id, "user_id": user_id})

async def get_pretenders(chat_id: int) -> List[int]:
    users = []
    async for x in pretdb.find({"chat_id": chat_id}):
        users.append(x["user_id"])
    return users
