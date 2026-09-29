from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from config import BANNED_USERS


@app.on_message(filters.command(["mention", "tag"]) & filters.group & ~BANNED_USERS)
async def mention_user(_, message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
        await message.reply_text(f"{u.mention} {text}".strip())
    elif len(message.command) > 1:
        await message.reply_text(" ".join(message.command[1:]))
    else:
        await message.reply_text("Reply to a user or give text.")
