from functools import wraps
from pyrogram import types
from TanuMusic import app, db, userbot


def checkUB(func):
    @wraps(func)
    async def wrapper(_, m: types.Message, *args, **kwargs):
        if not userbot.clients:
            return await m.reply_text("No assistant account connected. Set STRING_SESSION.")
        if m.chat.type.name not in ("GROUP", "SUPERGROUP"):
            return await m.reply_text("Use this command in a group.")
        return await func(_, m, *args, **kwargs)

    return wrapper
