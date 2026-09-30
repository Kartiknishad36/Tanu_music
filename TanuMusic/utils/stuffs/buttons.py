from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class BUTTONS(object):
    MBUTTON = [
        [
            InlineKeyboardButton("● ᴄʜᴀᴛ-ɢᴘᴛ ●", callback_data="mplus HELP_ChatGPT"),
            InlineKeyboardButton("● ɢʀᴏᴜᴘ ●", callback_data="mplus HELP_Group"),
            InlineKeyboardButton("● sᴛɪᴄᴋᴇʀ ●", callback_data="mplus HELP_Sticker"),
        ],
        [
            InlineKeyboardButton("● ᴛᴀɢᴀʟʟ ●", callback_data="mplus HELP_TagAll"),
            InlineKeyboardButton("● ɪɴғᴏ ●", callback_data="mplus HELP_Info"),
            InlineKeyboardButton("● ᴇxᴛʀᴀ ●", callback_data="mplus HELP_Extra"),
        ],
        [
            InlineKeyboardButton("● ᴀᴄᴛɪᴏɴ ●", callback_data="mplus HELP_Action"),
            InlineKeyboardButton("● sᴇᴀʀᴄʜ ●", callback_data="mplus HELP_Search"),
            InlineKeyboardButton("● ғᴜɴ ●", callback_data="mplus HELP_Fun"),
        ],
        [
            InlineKeyboardButton("● ғᴏɴᴛ ●", callback_data="mplus HELP_Font"),
            InlineKeyboardButton("● ɢᴀᴍᴇ ●", callback_data="mplus HELP_Game"),
            InlineKeyboardButton("● ᴛᴏᴏʟs ●", callback_data="mplus HELP_Tool"),
        ],
        [
            InlineKeyboardButton("◁", callback_data="settings_back_helper"),
            InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]

    BACK = [[InlineKeyboardButton("◁", callback_data="mbot_cb")]]

    HELP_BTN = [
        [
            InlineKeyboardButton("◁", callback_data="settings_back_helper"),
            InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
        ]
    ]
