import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("population"))
async def population_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /population IN")
    country_code = message.command[1].strip()
    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        country_info = response.json()
        country_name = country_info[0].get("name", {}).get("common", "N/A")
        capital = country_info[0].get("capital", ["N/A"])[0]
        population = country_info[0].get("population", "N/A")
        await message.reply_text(
            f"**{country_name}**\nCapital: {capital}\nPopulation: {population}"
        )
    except Exception as e:
        await message.reply_text(f"Error: {e}")
