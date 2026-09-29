from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import get_active_chats, get_active_video_chats


@app.on_message(filters.command(["activevc", "activevoice"]) & SUDOERS)
async def active_voice(_, message: Message):
    chats = await get_active_chats()
    text = f"**Active voice chats: {len(chats)}**\n"
    for i, chat_id in enumerate(chats, 1):
        try:
            title = (await app.get_chat(chat_id)).title
            text += f"{i}. {title} [`{chat_id}`]\n"
        except Exception:
            text += f"{i}. `{chat_id}`\n"
    await message.reply_text(text or "No active chats")


@app.on_message(filters.command(["activevideo", "activev"]) & SUDOERS)
async def active_video(_, message: Message):
    chats = await get_active_video_chats()
    text = f"**Active video chats: {len(chats)}**\n"
    for i, chat_id in enumerate(chats, 1):
        text += f"{i}. `{chat_id}`\n"
    await message.reply_text(text or "No active video chats")
