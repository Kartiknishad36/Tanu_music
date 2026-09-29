from pyrogram import filters
from TanuMusic import app

try:
    from gpytranslate import Translator

    trans = Translator()
except Exception:
    trans = None


@app.on_message(filters.command("tr"))
async def translate(_, message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        return await message.reply_text("Reply to a message to translate it!")
    to_translate = reply_msg.caption or reply_msg.text
    if not to_translate:
        return await message.reply_text("No text to translate.")
    if not trans:
        return await message.reply_text("gpytranslate not installed.")
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source, dest = args.split("//", 1)
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    await message.reply_text(f"Translated from {source} to {dest}:\n{translation.text}")
