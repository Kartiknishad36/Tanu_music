from pyrogram import filters, enums
from pyrogram.types import Message
from TanuMusic import app
from pyrogram.errors import FloodWait


@app.on_message(filters.command("unbanall") & filters.group)
async def unbanall(_, msg: Message):
    user = await app.get_chat_member(msg.chat.id, msg.from_user.id)
    if user.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await msg.reply_text("Only admins can use this.")
    m = await msg.reply_text("Unbanning all...")
    count = 0
    async for member in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.BANNED):
        try:
            await app.unban_chat_member(msg.chat.id, member.user.id)
            count += 1
        except FloodWait as e:
            import asyncio
            await asyncio.sleep(e.value)
        except Exception:
            pass
    await m.edit_text(f"Unbanned {count} users.")
