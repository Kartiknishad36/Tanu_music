from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["bots", "botschk"]) & filters.group)
async def bots_chk(_, message: Message):
    bots = []
    async for m in app.get_chat_members(message.chat.id, filter="bots"):
        bots.append(f"• {m.user.mention}")
    if not bots:
        return await message.reply_text("No bots found.")
    await message.reply_text("**Bots in this chat:**\n\n" + "\n".join(bots))
