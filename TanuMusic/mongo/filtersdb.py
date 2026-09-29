from typing import Dict, List, Union

from TanuMusic.core.mongo import mongodb

filtersdb = mongodb.filters


async def get_filters_count() -> dict:
    chats_count = 0
    filters_count = 0
    cursor = filtersdb.find({"chat_id": {"$lt": 0}})
    async for chat in cursor:
        filters_ = await get_filters(chat["chat_id"])
        if filters_:
            chats_count += 1
            filters_count += len(filters_)
    return {
        "chats_count": chats_count,
        "filters_count": filters_count,
    }


async def _get_filters(chat_id: int) -> Dict[str, int]:
    _filters = await filtersdb.find_one({"chat_id": chat_id})
    if _filters:
        return _filters["filters"]
    return {}


async def get_filters_names(chat_id: int) -> List[str]:
    _filters = await _get_filters(chat_id)
    return list(_filters.keys())


async def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    if name in _filters:
        return _filters[name]
    return False


async def get_filters(chat_id: int) -> Dict[str, int]:
    return await _get_filters(chat_id)


async def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = await _get_filters(chat_id)
    _filters[name] = _filter
    await filtersdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )


async def delete_filter(chat_id: int, name: str) -> bool:
    filtersd = await _get_filters(chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        await filtersdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"filters": filtersd}},
            upsert=True,
        )
        return True
    return False
