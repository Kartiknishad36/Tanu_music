import requests
from pyrogram import filters
from TanuMusic import app

JOKE_API_ENDPOINT = "https://hindi-jokes-api.onrender.com/jokes?api_key=1a6d440e3f5971eecebceee818c2"


@app.on_message(filters.command("hjoke"))
async def joke(_, message):
    try:
        response = requests.get(JOKE_API_ENDPOINT, timeout=15)
        r = response.json()
        joke_text = r.get("jokeContent") or str(r)
        await message.reply_text(joke_text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
