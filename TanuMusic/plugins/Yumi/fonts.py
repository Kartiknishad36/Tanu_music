from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from TanuMusic.utils.baby_font import Fonts
from TanuMusic import app


@app.on_message(filters.command(["font", "fonts"]))
async def style_buttons(c, m, cb=False):
    try:
        text = m.text.split(" ", 1)[1]
    except IndexError:
        return await m.reply_text("Usage: /font <text>")
    buttons = [
        [
            InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="style+typewriter"),
            InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="style+outline"),
            InlineKeyboardButton("𝙎𝙚𝙧𝙞𝙛", callback_data="style+serief"),
        ],
        [
            InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟 𝐁", callback_data="style+bold-serif"),
            InlineKeyboardButton("𝑆𝑒𝑟𝑖𝑓 𝐼", callback_data="style+italic-serif"),
            InlineKeyboardButton("𝑺𝒆𝒓𝒊𝒇 𝑩𝑰", callback_data="style+bold-italic-serif"),
        ],
        [
            InlineKeyboardButton("𝖲𝖺𝗇𝗌", callback_data="style+sans"),
            InlineKeyboardButton("𝗦𝗮𝗻𝘀 𝗕", callback_data="style+bold-sans"),
            InlineKeyboardButton("𝘚𝘢𝘯𝘴 𝘐", callback_data="style+italic-sans"),
        ],
        [
            InlineKeyboardButton("𝙎𝙖𝙣𝙨 𝘽𝙄", callback_data="style+bold-italic-sans"),
            InlineKeyboardButton("𝒞𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="style+script"),
            InlineKeyboardButton("𝓒𝓼𝓬𝓻𝓲𝓹𝓽 𝓑", callback_data="style+bold-script"),
        ],
        [
            InlineKeyboardButton("𝔡𝔬𝔲𝔟𝔩𝔢", callback_data="style+double"),
            InlineKeyboardButton("𝔠𝔬𝔰𝔪𝔦𝔠", callback_data="style+cosmic"),
            InlineKeyboardButton("🅑 🅒", callback_data="style+circle"),
        ],
        [
            InlineKeyboardButton("Close", callback_data="close"),
        ],
    ]
    if cb:
        await m.answer()
        await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
    else:
        await m.reply_text(f"`{text}`", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("^style"))
async def style(c, m):
    await m.answer()
    try:
        cmd, style = m.data.split("+")
        text = m.message.reply_to_message.text if m.message.reply_to_message else m.message.text
        if style == "typewriter":
            out = Fonts.typewriter(text)
        elif style == "outline":
            out = Fonts.outline(text)
        elif style == "serief":
            out = Fonts.serief(text)
        elif style == "bold-serif":
            out = Fonts.bold_serief(text)
        elif style == "italic-serif":
            out = Fonts.italic_serief(text)
        elif style == "bold-italic-serif":
            out = Fonts.bold_italic_serief(text)
        elif style == "sans":
            out = Fonts.sans(text)
        elif style == "bold-sans":
            out = Fonts.bold_sans(text)
        elif style == "italic-sans":
            out = Fonts.italic_sans(text)
        elif style == "bold-italic-sans":
            out = Fonts.bold_italic_sans(text)
        elif style == "script":
            out = Fonts.script(text)
        elif style == "bold-script":
            out = Fonts.bold_script(text)
        elif style == "double":
            out = Fonts.double(text)
        elif style == "cosmic":
            out = Fonts.cosmic(text)
        elif style == "circle":
            out = Fonts.circle(text)
        else:
            out = text
        await m.message.edit_text(out, reply_markup=m.message.reply_markup)
    except Exception as e:
        await m.message.reply_text(f"Error: {e}")
