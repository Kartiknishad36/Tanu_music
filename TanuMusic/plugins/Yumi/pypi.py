import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("pypi", prefixes="/"))
async def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
    except IndexError:
        return await message.reply_text("Usage: /pypi package_name")
    try:
        r = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=15)
        if r.status_code != 200:
            return await message.reply_text("Package not found.")
        info = r.json()["info"]
        text = (
            f"**Package:** {info.get('name')}\n"
            f"**Version:** {info.get('version')}\n"
            f"**Summary:** {info.get('summary')}\n"
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
