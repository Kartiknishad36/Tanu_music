from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["insta", "instagram"]))
async def insta_dl(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /insta <instagram_url>")
    url = message.command[1]
    await message.reply_text(
        f"Instagram URL received.\nUse yt-dlp compatible downloader for: {url}"
    )
