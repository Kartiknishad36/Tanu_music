from pyrogram import filters
import requests
from TanuMusic import app

bored_api_url = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command("bored", prefixes="/"))
async def bored_command(client, message):
    response = requests.get(bored_api_url)
    if response.status_code == 200:
        data = response.json()
        activity = data.get("activity")
        if activity:
            await message.reply(f"Feeling bored? How about:\n\n{activity}")
        else:
            await message.reply("No activity found.")
    else:
        await message.reply("Failed to fetch activity.")
