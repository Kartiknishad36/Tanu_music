from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.core.call import BABY
from TanuMusic.misc import db
from TanuMusic.utils.database import get_loop, set_loop
from TanuMusic.utils.decorators import AdminRightsCheck
from TanuMusic.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(filters.command(["skip", "cskip", "next"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def skip_track(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
    popped = None
    try:
        popped = check.pop(0)
        if popped:
            pass
        if not check:
            await BABY.stop_stream(chat_id)
            await set_loop(chat_id, 0)
            return await message.reply_text(
                _["admin_6"].format(message.from_user.mention),
                reply_markup=close_markup(_),
            )
    except Exception:
        try:
            await message.reply_text(_["admin_6"].format(message.from_user.mention))
            await BABY.stop_stream(chat_id)
            await set_loop(chat_id, 0)
        except Exception:
            pass
        return
    queued = check[0]["file"]
    title = check[0]["title"]
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    video = True if streamtype == "video" else False
    try:
        await BABY.skip_stream(chat_id, queued, video=video)
        await message.reply_text(
            f"Skipped\n**Now playing:** {title}\n**Requested by:** {user}",
            reply_markup=close_markup(_),
        )
    except Exception as e:
        await message.reply_text(f"Skip error: {e}")
