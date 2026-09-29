from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import (
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from TanuMusic.utils.decorators.language import language


@app.on_message(filters.command(["maintenance"]) & SUDOERS)
@language
async def maintenance(client, message: Message, _):
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text(_["maint_4"])
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"].format(app.mention))
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention))
        else:
            await message.reply_text(_["maint_5"])
    else:
        await message.reply_text(usage)
