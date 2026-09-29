import random
from pyrogram import filters
from TanuMusic import app

WISHES = [
    "Have a cute day 🌸",
    "Sending virtual hugs 🤗",
    "Stay sweet 💕",
    "You are awesome ✨",
]


@app.on_message(filters.command(["wish", "cute"]))
async def wish_cmd(_, message):
    target = message.reply_to_message.from_user.mention if message.reply_to_message else message.from_user.mention
    await message.reply_text(f"{target}, {random.choice(WISHES)}")
