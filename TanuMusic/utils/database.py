import random
from typing import Dict, List, Union

from TanuMusic import userbot
from TanuMusic.core.mongo import mongodb

authdb = mongodb.adminauth
authuserdb = mongodb.authuser
autoenddb = mongodb.autoend
assdb = mongodb.assistants
blacklist_chatdb = mongodb.blacklistChat
blockeddb = mongodb.blockedusers
chatsdb = mongodb.chats
channeldb = mongodb.cplaymode
countdb = mongodb.cleanmode
crossdb = mongodb.crossex
couplesdb = mongodb.couples
filtersdb = mongodb.filters
gbandb = mongodb.gban
onoffdb = mongodb.onoff
playmodedb = mongodb.playmode
playtypedb = mongodb.playtype
skipdb = mongodb.skip
sudoersdb = mongodb.sudoers
usersdb = mongodb.tgusersdb
vcdb = mongodb.vc
videodb = mongodb.videocalls
notesdb = mongodb.notes
cardsdb = mongodb.cards

# Active chats
active = []
activevideo = []

async def get_active_chats() -> list:
    return active

async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active

async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

async def get_active_video_chats() -> list:
    return activevideo

async def is_active_video_chat(chat_id: int) -> bool:
    return chat_id in activevideo

async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)

async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)

# Auth
async def is_nonadmin_chat(chat_id: int) -> bool:
    user = await authdb.find_one({"chat_id": chat_id})
    return bool(user)

async def add_nonadmin_chat(chat_id: int):
    is_auth = await is_nonadmin_chat(chat_id)
    if not is_auth:
        return await authdb.insert_one({"chat_id": chat_id})

async def remove_nonadmin_chat(chat_id: int):
    is_auth = await is_nonadmin_chat(chat_id)
    if is_auth:
        return await authdb.delete_one({"chat_id": chat_id})

# Auth users
async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if _notes:
        return _notes["notes"]
    return {}

async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes

async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    name = name
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    return False

async def save_authuser(chat_id: int, name: str, note: dict):
    name = name
    _notes = await _get_authusers(chat_id)
    _notes[name] = note
    await authuserdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )

async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    name = name
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False

# Assistants
async def get_assistant_number(chat_id: int) -> int:
    assistant = await assdb.find_one({"chat_id": chat_id})
    if not assistant:
        return 1
    return assistant["assistant"]

async def set_assistant_number(chat_id: int, mode: int):
    await assdb.update_one(
        {"chat_id": chat_id}, {"$set": {"assistant": mode}}, upsert=True
    )

async def get_assistant(chat_id: int) -> str:
    assistant = await get_assistant_number(chat_id)
    return getattr(userbot, f"one" if assistant == 1 else f"{['one','two','three','four','five'][assistant-1]}", userbot.one)

async def group_assistant(call, chat_id: int):
    assistant = await get_assistant_number(chat_id)
    if assistant == 1:
        return call.one
    elif assistant == 2:
        return call.two
    elif assistant == 3:
        return call.three
    elif assistant == 4:
        return call.four
    elif assistant == 5:
        return call.five
    return call.one

# Blacklist
async def blacklisted_chats() -> list:
    chats = blacklist_chatdb.find({"chat_id": {"$lt": 0}})
    return [chat["chat_id"] async for chat in chats]

async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False

async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False

# Blocked users
async def get_gbanned() -> list:
    results = []
    async for user in gbandb.find({"user_id": {"$gt": 0}}):
        results.append(user["user_id"])
    return results

async def is_gbanned_user(user_id: int) -> bool:
    return bool(await gbandb.find_one({"user_id": user_id}))

async def add_gban_user(user_id: int):
    if not await is_gbanned_user(user_id):
        return await gbandb.insert_one({"user_id": user_id})

async def remove_gban_user(user_id: int):
    if await is_gbanned_user(user_id):
        return await gbandb.delete_one({"user_id": user_id})

# Served chats / users
async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    return bool(chat)

async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    return [chat["chat_id"] async for chat in chats]

async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if not is_served:
        return await chatsdb.insert_one({"chat_id": chat_id})

async def remove_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return await chatsdb.delete_one({"chat_id": chat_id})

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)

async def get_served_users() -> list:
    users = usersdb.find({"user_id": {"$gt": 0}})
    return [user["user_id"] async for user in users]

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if not is_served:
        return await usersdb.insert_one({"user_id": user_id})

# Sudoers
async def get_sudoers() -> list:
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    if not sudoers:
        return []
    return sudoers["sudoers"]

async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True

async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await sudoersdb.update_one(
        {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
    )
    return True

# Play mode / type
async def get_playmode(chat_id: int) -> str:
    mode = await playmodedb.find_one({"chat_id": chat_id})
    if not mode:
        return "Direct"
    return mode["mode"]

async def set_playmode(chat_id: int, mode: str):
    await playmodedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def get_playtype(chat_id: int) -> str:
    mode = await playtypedb.find_one({"chat_id": chat_id})
    if not mode:
        return "Everyone"
    return mode["mode"]

async def set_playtype(chat_id: int, mode: str):
    await playtypedb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

# Autoend
async def is_autoend() -> bool:
    chat = await autoenddb.find_one({"autoend": "on"})
    return bool(chat)

async def autoend_on():
    return await autoenddb.insert_one({"autoend": "on"})

async def autoend_off():
    return await autoenddb.delete_one({"autoend": "on"})

# Loop / music on-off
loop = {}

async def get_loop(chat_id: int) -> int:
    return loop.get(chat_id, 0)

async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode

async def music_on(chat_id: int):
    onoff = await onoffdb.find_one({"chat_id": chat_id})
    if not onoff:
        return await onoffdb.insert_one({"chat_id": chat_id})

async def music_off(chat_id: int):
    onoff = await onoffdb.find_one({"chat_id": chat_id})
    if onoff:
        return await onoffdb.delete_one({"chat_id": chat_id})

async def is_music_playing(chat_id: int) -> bool:
    return bool(await onoffdb.find_one({"chat_id": chat_id}))

# Lang
async def get_lang(chat_id: int) -> str:
    from strings import get_string
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if chat and "lang" in chat:
        return chat["lang"]
    return "en"

async def set_lang(chat_id: int, lang: str):
    await chatsdb.update_one(
        {"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True
    )

# Channel play
async def get_cmode(chat_id: int) -> int:
    mode = await channeldb.find_one({"chat_id": chat_id})
    if not mode:
        return None
    return mode["mode"]

async def set_cmode(chat_id: int, mode: int):
    await channeldb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

# Skip / cleanmode stubs
async def is_skip(chat_id: int) -> bool:
    return bool(await skipdb.find_one({"chat_id": chat_id}))

async def skip_on(chat_id: int):
    if not await is_skip(chat_id):
        return await skipdb.insert_one({"chat_id": chat_id})

async def skip_off(chat_id: int):
    if await is_skip(chat_id):
        return await skipdb.delete_one({"chat_id": chat_id})

# Cards (fun)
async def is_card_exists(cc: str) -> bool:
    return bool(await cardsdb.find_one({"cc": cc}))

async def add_card(cc: str):
    if not await is_card_exists(cc):
        return await cardsdb.insert_one({"cc": cc})

async def remove_card(cc: str):
    is_exist = await is_card_exists(cc)
    if not is_exist:
        return
    return await cardsdb.delete_one({"cc": cc})
