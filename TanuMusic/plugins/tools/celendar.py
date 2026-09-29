from datetime import datetime
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["date", "time", "calendar"]))
async def date_cmd(_, message):
    now = datetime.now()
    await message.reply_text(
        f"**Date:** {now.strftime('%d %B %Y')}\n**Time:** {now.strftime('%I:%M:%S %p')}\n**Day:** {now.strftime('%A')}"
    )
