from random import choice

import pyfiglet
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from TanuMusic import app

text = ""


def figle(text_in):
    fonts = pyfiglet.FigletFont.getFonts()
    font = choice(fonts)
    figled = str(pyfiglet.figlet_format(text_in, font=font))
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Change", callback_data="figlet"),
                InlineKeyboardButton(text="Close", callback_data="close_reply"),
            ]
        ]
    )
    return figled, keyboard


@app.on_message(filters.command("figlet"))
async def echo(bot, message):
    global text
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply_text("Example:\n\n`/figlet Tanu Music`")
    kul_text, keyboard = figle(text)
    await message.reply_text(
        f"Here is your figlet:\n<pre>{kul_text}</pre>",
        quote=True,
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("figlet"))
async def figlet_handler(Client, query: CallbackQuery):
    try:
        kul_text, keyboard = figle(text)
        await query.message.edit_text(
            f"Here is your figlet:\n<pre>{kul_text}</pre>", reply_markup=keyboard
        )
    except Exception as e:
        await query.message.reply_text(str(e))
