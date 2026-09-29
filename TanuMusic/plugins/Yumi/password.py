import random
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from TanuMusic import app


@app.on_message(filters.command(["genpassword", "genpw"]))
async def password(bot, update):
    message = await update.reply_text(text="Processing..")
    password_chars = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    if len(update.command) > 1:
        qw = update.text.split(" ", 1)[1]
    else:
        ST = ["5", "7", "6", "9", "10", "12", "14", "8", "13"]
        qw = random.choice(ST)
    limit = int(qw)
    random_value = "".join(random.sample(password_chars, limit))
    txt = f"<b>Limit:</b> {str(limit)} \n<b>Password: <code>{random_value}</code>"
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Add Me", url="https://t.me/KARTIK_NISHAD_3")]]
    )
    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
