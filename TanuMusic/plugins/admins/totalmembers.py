from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["members", "totalmembers"]) & filters.group)
async def total_members(_, message: Message):
    try:
        count = await app.get_chat_members_count(message.chat.id)
        await message.reply_text(f"Total members: **{count}**")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
