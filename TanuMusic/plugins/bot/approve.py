from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.misc import SUDOERS


@app.on_message(filters.command(["approve", "disapprove"]) & SUDOERS)
async def approve_cmd(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a join request / user.")
    try:
        user = message.reply_to_message.from_user
        if message.command[0].lower() == "approve":
            await app.approve_chat_join_request(message.chat.id, user.id)
            await message.reply_text(f"Approved {user.mention}")
        else:
            await app.decline_chat_join_request(message.chat.id, user.id)
            await message.reply_text(f"Disapproved {user.mention}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
