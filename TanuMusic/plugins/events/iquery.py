from pyrogram import types
from TanuMusic import app

@app.on_inline_query(~app.bl_users)
async def inline_query_handler(_, query: types.InlineQuery):
    # Inline search optional — enable later with yt-dlp
    await query.answer([], cache_time=1)
