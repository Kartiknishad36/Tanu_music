import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("webdl"))
async def web_download(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /webdl https://example.com")
    url = message.command[1]
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            timeout=20,
        )
        if response.status_code != 200:
            return await message.reply_text(f"Failed: HTTP {response.status_code}")
        with open("website.txt", "w", encoding="utf-8") as file:
            file.write(response.text)
        await message.reply_document(document="website.txt", caption=f"Source of {url}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
