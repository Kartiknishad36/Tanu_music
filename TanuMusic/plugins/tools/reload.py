import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.utils.database import get_authuser_names, get_authuser
from TanuMusic.utils.decorators import language
from TanuMusic.utils.formatters import alpha_to_int
from config import BANNED_USERS, adminlist


@app.on_message(filters.command(["reload", "admincache", "refresh"]) & filters.group & ~BANNED_USERS)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        adminlist[chat_id] = []
        async for user in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if user.privileges.can_manage_video_chats:
                adminlist[chat_id].append(user.user.id)
        authusers = await get_authuser_names(chat_id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_12"] if "admin_12" in _ else "Admin cache reloaded.")
    except Exception:
        await message.reply_text("Failed to reload admin cache.")
