"""Leave chat command stub."""
from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.misc import SUDOERS
from config import BANNED_USERS


@app.on_message(filters.command(["leave"]) & ~BANNED_USERS)
async def leave_cmd(_, m: Message):
    if m.from_user.id not in SUDOERS:
        return
    try:
        await m.reply_text("Leaving chat...")
        await app.leave_chat(m.chat.id)
    except Exception as e:
        await m.reply_text(f"Error: {e}")
