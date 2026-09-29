from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.mongo.nightmodedb import nightmode_off, nightmode_on, get_nightchats
from TanuMusic.utils.baby_ban import admin_filter


@app.on_message(filters.command(["nightmode"]) & admin_filter)
async def nightmode_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /nightmode on|off")
    arg = message.command[1].lower()
    if arg == "on":
        await nightmode_on(message.chat.id)
        await message.reply_text("Night mode ON")
    elif arg == "off":
        await nightmode_off(message.chat.id)
        await message.reply_text("Night mode OFF")
    else:
        await message.reply_text("Usage: /nightmode on|off")
