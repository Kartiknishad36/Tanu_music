"""Autoleave handled via config AUTO_LEAVING_ASSISTANT."""
from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.misc import SUDOERS
from config import BANNED_USERS


@app.on_message(filters.command(["autoleave"]) & filters.group & ~BANNED_USERS)
async def autoleave_command(_, m: Message):
    if m.from_user.id not in SUDOERS:
        return await m.reply_text("Only sudo users can use this.")
    await m.reply_text(
        "Auto-leave is controlled by Railway env:\n"
        "`AUTO_LEAVING_ASSISTANT=True/False`"
    )
