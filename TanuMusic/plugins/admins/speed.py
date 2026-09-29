from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import db
from TanuMusic.utils.database import is_active_chat, is_nonadmin_chat
from TanuMusic.utils.decorators import AdminRightsCheck, languageCB
from TanuMusic.utils.inline.speed import speed_markup
from TanuMusic.misc import SUDOERS
from config import BANNED_USERS, adminlist


@app.on_message(
    filters.command(["speed", "cspeed", "playback", "cplayback"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def playback(cli, message: Message, _, chat_id):
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    if int(playing[0]["seconds"]) == 0:
        return await message.reply_text(_["admin_27"])
    if "downloads" not in playing[0]["file"]:
        return await message.reply_text(_["admin_27"])
    return await message.reply_text(
        text=_["admin_28"].format(app.mention),
        reply_markup=speed_markup(_, chat_id),
    )
