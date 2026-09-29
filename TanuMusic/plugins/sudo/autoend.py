from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import autoend_off, autoend_on


@app.on_message(filters.command("autoend") & SUDOERS)
async def auto_end_stream(_, message: Message):
    usage = "<b>Example:</b>\n\n/autoend [enable | disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Auto end stream enabled.\nAssistant will leave VC after a few mins when no one is listening."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Auto end stream disabled.")
    else:
        await message.reply_text(usage)
