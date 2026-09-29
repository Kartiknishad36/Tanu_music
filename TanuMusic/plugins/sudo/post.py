from pyrogram import filters

from TanuMusic import app
from config import OWNER_ID


@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(_, message):
    if message.reply_to_message:
        destination_group_id = message.chat.id
        await message.reply_to_message.copy(destination_group_id)
        await message.reply("Post successful.")
    else:
        await message.reply("Reply to a message to post/copy it.")
