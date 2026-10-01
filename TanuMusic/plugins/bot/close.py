from pyrogram import filters
from pyrogram.types import CallbackQuery

from TanuMusic import app
from config import BANNED_USERS


@app.on_callback_query(filters.regex("^close$") & ~BANNED_USERS)
async def close_menu(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except Exception:
        try:
            await query.answer("Closed")
            await query.message.edit_reply_markup(None)
        except Exception:
            pass
