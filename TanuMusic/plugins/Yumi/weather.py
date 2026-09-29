from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("weather"))
async def weather(client, message):
    try:
        location = message.command[1].strip()
        weather_url = f"https://wttr.in/{location}.png"
        await message.reply_photo(
            photo=weather_url, caption=f"Weather for {location}"
        )
    except IndexError:
        await message.reply_text("Usage: /weather Delhi")
