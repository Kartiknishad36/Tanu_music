from pyrogram import filters, enums
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["zombies", "cleanzombies"]) & filters.group)
async def zombies_clean(client, message: Message):
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("Admins only.")
    m = await message.reply_text("Cleaning deleted accounts...")
    count = 0
    async for member in client.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            try:
                await client.ban_chat_member(message.chat.id, member.user.id)
                await client.unban_chat_member(message.chat.id, member.user.id)
                count += 1
            except Exception:
                pass
    await m.edit_text(f"Cleaned {count} deleted accounts.")
