import requests
from pyrogram import filters
from TanuMusic import app

truth_api_url = "https://api.truthordarebot.xyz/v1/truth"
dare_api_url = "https://api.truthordarebot.xyz/v1/dare"


@app.on_message(filters.command("truth"))
async def get_truth(client, message):
    try:
        response = requests.get(truth_api_url, timeout=15)
        if response.status_code == 200:
            await message.reply_text(f"Truth:\n\n{response.json()['question']}")
        else:
            await message.reply_text("Failed to fetch truth question.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")


@app.on_message(filters.command("dare"))
async def get_dare(client, message):
    try:
        response = requests.get(dare_api_url, timeout=15)
        if response.status_code == 200:
            await message.reply_text(f"Dare:\n\n{response.json()['question']}")
        else:
            await message.reply_text("Failed to fetch dare.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
