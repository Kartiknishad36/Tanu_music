from pyrogram import filters
from pyrogram.types import InlineQuery

from TanuMusic import app
from config import BANNED_USERS


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(_, query: InlineQuery):
    try:
        await query.answer([], cache_time=1)
    except Exception:
        pass
