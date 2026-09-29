import pycountry
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("get_states"))
async def get_states(client, message):
    try:
        country_name = message.text.split(" ", 1)[1]
        country = pycountry.countries.get(name=country_name) or pycountry.countries.search_fuzzy(country_name)[0]
        states = list(pycountry.subdivisions.get(country_code=country.alpha_2))
        text = f"**States of {country.name}:**\n" + "\n".join(
            f"• {s.name}" for s in states[:50]
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}\nUsage: /get_states India")
