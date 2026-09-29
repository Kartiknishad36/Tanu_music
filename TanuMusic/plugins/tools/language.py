from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from TanuMusic import app
from TanuMusic.utils.database import get_lang, set_lang
from TanuMusic.utils.decorators import language
from config import BANNED_USERS
from strings import get_string, languages_present


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def language_cmd(client, message: Message, _):
    buttons = [
        [InlineKeyboardButton(text=v, callback_data=f"languages_{k}")]
        for k, v in languages_present.items()
    ]
    buttons.append([InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")])
    await message.reply_text(
        _["lang_1"] if "lang_1" in _ else "Choose language:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(r"languages_"))
async def language_cb(client, callback):
    lang = callback.data.split("_", 1)[1]
    await set_lang(callback.message.chat.id, lang)
    _ = get_string(lang)
    await callback.message.edit_text(
        _["lang_2"].format(languages_present.get(lang, lang))
        if "lang_2" in _
        else f"Language set to {lang}"
    )
