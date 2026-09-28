import asyncio
import logging
from pyrogram import filters, types
from pyrogram.errors import ChatSendPlainForbidden, ChatWriteForbidden

from TanuMusic import tune, app, db, lang
from TanuMusic.helpers import can_manage_vc

logger = logging.getLogger(__name__)


@app.on_message(filters.command(["skip", "next"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _skip(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    if not await db.get_call(m.chat.id):
        try:
            return await m.reply_text(m.lang["not_playing"])
        except (ChatSendPlainForbidden, ChatWriteForbidden):
            return

    await tune.play_next(m.chat.id)
    try:
        sent_msg = await m.reply_text(m.lang["play_skipped"].format(m.from_user.mention))
    except (ChatSendPlainForbidden, ChatWriteForbidden):
        logger.warning("Cannot send plain text in media-only chat")
        return

    await asyncio.sleep(5)
    try:
        await sent_msg.delete()
    except Exception:
        pass
