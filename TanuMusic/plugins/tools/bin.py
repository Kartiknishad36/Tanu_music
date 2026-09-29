import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["bin", "ccbin"]))
async def bin_lookup(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /bin 515462")
    binn = message.command[1][:6]
    try:
        r = requests.get(f"https://lookup.binlist.net/{binn}", timeout=10)
        if r.status_code != 200:
            return await message.reply_text("BIN not found.")
        data = r.json()
        text = (
            f"**BIN:** `{binn}`\n"
            f"**Brand:** {data.get('scheme')}\n"
            f"**Type:** {data.get('type')}\n"
            f"**Bank:** {data.get('bank', {}).get('name')}\n"
            f"**Country:** {data.get('country', {}).get('name')}\n"
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
