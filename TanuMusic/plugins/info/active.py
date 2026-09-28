# ===============================================================================
# active.py - Active Calls
# ===============================================================================
import os
from pyrogram import filters, types
from TanuMusic import app, db, lang, queue


@app.on_message(filters.command(["ac"]) & app.sudo_filter)
@lang.language()
async def _ac(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    if not db.active_calls:
        return await m.reply_text(m.lang["vc_empty"])

    return await m.reply_text(m.lang["vc_count"].format(len(db.active_calls)))
