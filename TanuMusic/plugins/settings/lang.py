from pyrogram import filters, types
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from TanuMusic import app, db, lang
from TanuMusic.core.lang import lang_codes


def get_lang_keyboard():
    rows = []
    row = []
    for code, name in lang_codes.items():
        row.append(InlineKeyboardButton(name, callback_data=f"set_lang_{code}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


@app.on_message(filters.command(["lang", "language"]) & ~app.bl_users)
@lang.language()
async def lang_menu(_, message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(message.lang.get("lang_group_only", "Groups only"))
    await message.reply_text(
        message.lang.get("lang_menu_title", "Select language:"),
        reply_markup=get_lang_keyboard(),
    )


@app.on_callback_query(filters.regex(r"^set_lang_") & ~app.bl_users)
@lang.language()
async def set_lang_callback(client, query: types.CallbackQuery):
    try:
        lang_code = query.data.split("_")[2]
    except IndexError:
        return await query.answer("Invalid", show_alert=True)
    if lang_code not in lang_codes:
        return await query.answer("Unsupported", show_alert=True)
    await db.set_lang(query.message.chat.id, lang_code)
    name = lang_codes[lang_code]
    try:
        await query.message.edit_text(f"Language set to {name}")
    except Exception:
        pass
    await query.answer("OK")
