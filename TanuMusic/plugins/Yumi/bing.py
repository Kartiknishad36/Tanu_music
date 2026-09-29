import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["bing", "img"]))
async def bing_img(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /bing query")
    query = " ".join(message.command[1:])
    await message.reply_text(f"Search: {query}\n\nUse Google/Bing manually for now.")
