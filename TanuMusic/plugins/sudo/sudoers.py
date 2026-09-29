from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import add_sudo, get_sudoers, remove_sudo
from config import OWNER_ID


@app.on_message(filters.command(["addsudo"]) & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give ID")
    user_id = (
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else int(message.command[1])
    )
    await add_sudo(user_id)
    SUDOERS.add(user_id)
    await message.reply_text(f"Added `{user_id}` to sudo")


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a user or give ID")
    user_id = (
        message.reply_to_message.from_user.id
        if message.reply_to_message
        else int(message.command[1])
    )
    await remove_sudo(user_id)
    SUDOERS.discard(user_id)
    await message.reply_text(f"Removed `{user_id}` from sudo")


@app.on_message(filters.command(["sudolist", "sudoers"]) & SUDOERS)
async def sudoers_list(_, message: Message):
    text = "**Sudo users:**\n"
    for user_id in sorted(SUDOERS):
        try:
            user = await app.get_users(user_id)
            text += f"• {user.mention} (`{user_id}`)\n"
        except Exception:
            text += f"• `{user_id}`\n"
    await message.reply_text(text)
