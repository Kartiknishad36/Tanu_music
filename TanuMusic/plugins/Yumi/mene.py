from pyrogram import filters
import requests
from TanuMusic import app


@app.on_message(filters.command("meme"))
async def meme_command(client, message):
    api_url = "https://meme-api.com/gimme"
    try:
        response = requests.get(api_url)
        data = response.json()
        meme_url = data.get("url")
        title = data.get("title")
        me = await app.get_me()
        caption = f"{title}\n\nRequest by {message.from_user.mention}\nBot: @{me.username}"
        await message.reply_photo(photo=meme_url, caption=caption)
    except Exception:
        await message.reply_text("Sorry, could not fetch a meme right now.")
