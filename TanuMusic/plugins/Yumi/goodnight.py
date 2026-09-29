import random
from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app

STICKERS = [
    "CAACAgQAAx0Ce9_hCAACaEVlwn7HeZhgwyVfKHc3WUGC_447IAACLgwAAkQwKVPtub8VAR018x4E",
    "CAACAgIAAx0Ce9_hCAACaEplwn7dvj7G0-a1v3wlbN281RMX2QACUgwAAligOUoi7DhLVTsNsh4E",
]
EMOJIS = ["😴", "😪", "💤"]


@app.on_message(filters.command(["goodnight", "gn"]))
async def goodnight_command_handler(client, message: Message):
    if random.choice([True, False]):
        try:
            await client.send_sticker(message.chat.id, random.choice(STICKERS))
        except Exception:
            await message.reply_text(random.choice(EMOJIS))
    else:
        await message.reply_text(random.choice(EMOJIS))
