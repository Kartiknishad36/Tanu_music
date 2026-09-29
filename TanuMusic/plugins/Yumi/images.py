import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["image", "img"]))
async def image_search(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /image query")
    query = " ".join(message.command[1:])
    await message.reply_text(f"Searching images for: **{query}**\n\n(Use external image APIs if configured)")
