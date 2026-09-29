import random
import requests
from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


def calculate_gay_percentage():
    return random.randint(1, 100)


def generate_gay_response(gay_percentage):
    if gay_percentage < 30:
        return "You're straight as an arrow."
    elif 30 <= gay_percentage < 70:
        return "You might have a bit of a rainbow in you."
    else:
        return "You're shining with rainbow colors!"


@app.on_message(filters.command("gay"))
async def gay_calculator_command(client, message: Message):
    gay_percentage = calculate_gay_percentage()
    gay_response = generate_gay_response(gay_percentage)
    await message.reply_text(f"Gay Percentage: {gay_percentage}%\n{gay_response}")


@app.on_message(filters.command("logo"))
async def logo(app, msg: Message):
    if len(msg.command) == 1:
        return await msg.reply_text("Usage:\n\n/logo TEXT")
    logo_name = msg.text.split(" ", 1)[1]
    API = f"https://api.sdbots.tech/logohq?text={logo_name}"
    req = requests.get(API).url
    await msg.reply_photo(photo=f"{req}")


@app.on_message(filters.command("animelogo"))
async def animelogo(app, msg: Message):
    if len(msg.command) == 1:
        return await msg.reply_text("Usage:\n\n/animelogo TEXT")
    logo_name = msg.text.split(" ", 1)[1]
    API = f"https://api.sdbots.tech/anime-logo?name={logo_name}"
    req = requests.get(API).url
    await msg.reply_photo(photo=f"{req}")
