from pyrogram import filters, types
from TanuMusic import app, lang


@app.on_message(filters.command(["leave"]) & app.sudo_filter)
@lang.language()
async def leave_cmd(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass
    await m.reply_text("Leaving chat...")
    await app.leave_chat(m.chat.id)
