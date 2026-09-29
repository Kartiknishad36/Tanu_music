from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.misc import SUDOERS
from config import LOGGER_ID


@app.on_message(filters.command(["chatlog"]) & SUDOERS)
async def chatlog_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to log it.")
    try:
        await message.reply_to_message.forward(LOGGER_ID)
        await message.reply_text("Logged to log group.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
