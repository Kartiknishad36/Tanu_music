from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["groupinfo", "chatinfo"]) & filters.group)
async def group_info(_, message: Message):
    chat = message.chat
    try:
        full = await app.get_chat(chat.id)
        text = (
            f"**Title:** {full.title}\n"
            f"**ID:** `{full.id}`\n"
            f"**Type:** {full.type}\n"
            f"**Members:** {await app.get_chat_members_count(chat.id)}\n"
            f"**Username:** @{full.username if full.username else 'None'}\n"
            f"**Description:** {full.description or 'None'}\n"
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
