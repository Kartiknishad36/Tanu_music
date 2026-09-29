import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["ip", "ipinfo"]))
async def ip_info(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /ip 1.1.1.1")
    ip = message.command[1]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        text = (
            f"**IP:** {r.get('query')}\n"
            f"**Country:** {r.get('country')}\n"
            f"**Region:** {r.get('regionName')}\n"
            f"**City:** {r.get('city')}\n"
            f"**ISP:** {r.get('isp')}\n"
            f"**Org:** {r.get('org')}\n"
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
