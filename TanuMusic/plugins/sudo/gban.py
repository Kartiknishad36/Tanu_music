from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import (
    add_gban_user,
    get_served_chats,
    is_gbanned_user,
    remove_gban_user,
)
from config import BANNED_USERS


@app.on_message(filters.command(["gban"]) & SUDOERS)
async def gban_user(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give ID")
    user_id = (
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else int(message.command[1])
    )
    if await is_gbanned_user(user_id):
        return await message.reply_text("Already gbanned")
    await add_gban_user(user_id)
    BANNED_USERS.add(user_id)
    chats = await get_served_chats()
    banned = 0
    for chat_id in chats:
        try:
            await app.ban_chat_member(chat_id, user_id)
            banned += 1
        except Exception:
            pass
    await message.reply_text(f"GBanned `{user_id}` in {banned} chats")


@app.on_message(filters.command(["ungban"]) & SUDOERS)
async def ungban_user(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give ID")
    user_id = (
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else int(message.command[1])
    )
    await remove_gban_user(user_id)
    BANNED_USERS.discard(user_id)
    await message.reply_text(f"Ungbanned `{user_id}`")
