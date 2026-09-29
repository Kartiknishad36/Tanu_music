from pyrogram import filters
from TanuMusic import app

GN_MSG = [
    "Good Night 🌙 Sleep well",
    "Sweet dreams 💫",
    "Good night, take rest 🌟",
    "Night night 😴",
    "Have a peaceful night 🌌",
]

@app.on_message(filters.command(["gn", "goodnight", "night"]))
async def goodnight(client, message):
    import random
    await message.reply(random.choice(GN_MSG))
