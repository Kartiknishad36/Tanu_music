from typing import Dict, List, Union

from TanuMusic.core.mongo import mongodb

notesdb = mongodb.notes


async def get_notes_count() -> dict:
    chats_count = 0
    notes_count = 0
    async for chat in notesdb.find({"chat_id": {"$lt": 0}}):
        notes_ = await get_notes(chat["chat_id"])
        if notes_:
            chats_count += 1
            notes_count += len(notes_)
    return {"chats_count": chats_count, "notes_count": notes_count}


async def _get_notes(chat_id: int) -> Dict[str, int]:
    _notes = await notesdb.find_one({"chat_id": chat_id})
    if _notes:
        return _notes["notes"]
    return {}


async def get_note_names(chat_id: int) -> List[str]:
    _notes = await _get_notes(chat_id)
    return list(_notes.keys())


async def get_note(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    if name in _notes:
        return _notes[name]
    return False


async def get_notes(chat_id: int) -> Dict[str, int]:
    return await _get_notes(chat_id)


async def save_note(chat_id: int, name: str, note: dict):
    name = name.lower().strip()
    _notes = await _get_notes(chat_id)
    _notes[name] = note
    await notesdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"notes": _notes}},
        upsert=True,
    )


async def delete_note(chat_id: int, name: str) -> bool:
    notesd = await _get_notes(chat_id)
    name = name.lower().strip()
    if name in notesd:
        del notesd[name]
        await notesdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False
