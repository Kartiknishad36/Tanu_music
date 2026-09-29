from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["id", "userid"]))
async def userid_cmd(_, message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        u = message.reply_to_message.from_user
        return await message.reply_text(
            f"**User:** {u.mention}\n**ID:** `{u.id}`\n**Chat:** `{message.chat.id}`"
        )
    await message.reply_text(
        f"**Your ID:** `{message.from_user.id}`\n**Chat ID:** `{message.chat.id}`"
    )
