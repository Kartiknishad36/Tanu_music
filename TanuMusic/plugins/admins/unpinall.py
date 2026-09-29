from pyrogram import filters, enums
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command("unpinall") & filters.group)
async def unpin_all(_, message: Message):
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("Admins only.")
    try:
        await app.unpin_all_chat_messages(message.chat.id)
        await message.reply_text("All messages unpinned.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
