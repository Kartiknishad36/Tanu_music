from TanuMusic.core.mongo import mongodb

imposterdb = mongodb.imposter


async def is_imposter(chat_id: int) -> bool:
    return bool(await imposterdb.find_one({"chat_id": chat_id}))


async def set_imposter(chat_id: int):
    if not await is_imposter(chat_id):
        return await imposterdb.insert_one({"chat_id": chat_id})


async def rem_imposter(chat_id: int):
    if await is_imposter(chat_id):
        return await imposterdb.delete_one({"chat_id": chat_id})


async def get_imposter_users(chat_id: int):
    data = await imposterdb.find_one({"chat_id": chat_id})
    if data and "users" in data:
        return data["users"]
    return {}


async def add_imposter_user(chat_id: int, user_id: int, username: str):
    users = await get_imposter_users(chat_id)
    users[str(user_id)] = username
    await imposterdb.update_one(
        {"chat_id": chat_id}, {"$set": {"users": users}}, upsert=True
    )
