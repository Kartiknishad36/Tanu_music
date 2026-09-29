from pyrogram import filters
from TanuMusic import app
from config import BOT_USERNAME


def hex_to_text(hex_string):
    try:
        return bytes.fromhex(hex_string.replace(" ", "")).decode("utf-8")
    except Exception as e:
        return f"Error decoding hex: {e}"


def text_to_hex(text):
    return " ".join(format(ord(char), "x") for char in text)


@app.on_message(filters.command("code"))
async def convert_text(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /code your text")
    input_text = " ".join(message.command[1:])
    hex_representation = text_to_hex(input_text)
    decoded_text = hex_to_text(input_text)
    response_text = (
        f"Input: {input_text}\n"
        f"Hex: {hex_representation}\n"
        f"Decoded: {decoded_text}\n"
        f"By @{BOT_USERNAME}"
    )
    await message.reply_text(response_text)
