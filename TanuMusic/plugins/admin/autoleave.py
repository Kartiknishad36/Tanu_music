from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from config import BANNED_USERS


@app.on_message(filters.command(["autoleave"]) & filters.group & ~BANNED_USERS)
async def autoleave_command(_, m: Message):
    if m.from_user.id not in SUDOERS:
        return await m.reply_text("Only sudo users can use this command.")

    if len(m.command) < 2:
        return await m.reply_text(
            "**Usage:**\n"
            "• `/autoleave enable`\n"
            "• `/autoleave disable`\n\n"
            "(Auto-leave is controlled via config AUTO_LEAVING_ASSISTANT)"
        )

    sub = m.command[1].lower()
    if sub == "enable":
        await m.reply_text(
            "Auto leave is managed by env `AUTO_LEAVING_ASSISTANT`. "
            "Set it to True in Railway variables and restart."
        )
    elif sub == "disable":
        await m.reply_text(
            "Set env `AUTO_LEAVING_ASSISTANT=False` in Railway and restart."
        )
    else:
        await m.reply_text("Use `/autoleave enable` or `/autoleave disable`")
