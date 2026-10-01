from typing import Union

from pyrogram.types import InlineKeyboardButton


def setting_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text="🔐  ᴀᴜᴛʜ ᴜsᴇʀs", callback_data="AU"),
            InlineKeyboardButton(text="🌐  ʟᴀɴɢᴜᴀɢᴇ", callback_data="LG"),
        ],
        [
            InlineKeyboardButton(text="▶️  ᴘʟᴀʏ ᴍᴏᴅᴇ", callback_data="PM"),
        ],
        [
            InlineKeyboardButton(text="📊  ᴠᴏᴛᴇ ᴍᴏᴅᴇ", callback_data="VM"),
        ],
        [
            InlineKeyboardButton(text="✦  ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    status = "🟢  ᴏɴ" if mode else "🔴  ᴏғғ"
    buttons = [
        [
            InlineKeyboardButton(text="📊  ᴠᴏᴛɪɴɢ ᴍᴏᴅᴇ", callback_data="VOTEANSWER"),
            InlineKeyboardButton(text=status, callback_data="VOMODECHANGE"),
        ],
        [
            InlineKeyboardButton(text="➖  -2", callback_data="FERRARIUDTI M"),
            InlineKeyboardButton(
                text=f"💎  ᴄᴜʀʀᴇɴᴛ : {current}",
                callback_data="ANSWERVOMODE",
            ),
            InlineKeyboardButton(text="➕  +2", callback_data="FERRARIUDTI A"),
        ],
        [
            InlineKeyboardButton(text="◁  ʙᴀᴄᴋ", callback_data="settings_helper"),
            InlineKeyboardButton(text="✦  ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    st = "🟢  ᴇɴᴀʙʟᴇᴅ" if status else "🔴  ᴅɪsᴀʙʟᴇᴅ"
    buttons = [
        [
            InlineKeyboardButton(text="🔐  ᴀᴜᴛʜ ᴜsᴇʀs", callback_data="AUTHANSWER"),
            InlineKeyboardButton(text=st, callback_data="AUTH"),
        ],
        [
            InlineKeyboardButton(text="📋  ᴀᴜᴛʜ ʟɪsᴛ", callback_data="AUTHLIST"),
        ],
        [
            InlineKeyboardButton(text="◁  ʙᴀᴄᴋ", callback_data="settings_helper"),
            InlineKeyboardButton(text="✦  ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    d = "🟢  ᴅɪʀᴇᴄᴛ" if Direct else "🔵  ɪɴʟɪɴᴇ"
    g = "🟢  ɢʀᴏᴜᴘ" if Group else "🔵  ᴄʜᴀɴɴᴇʟ"
    p = "🟢  ᴇᴠᴇʀʏᴏɴᴇ" if Playtype else "🔴  ᴀᴅᴍɪɴ"
    buttons = [
        [
            InlineKeyboardButton(text="🎯  sᴇᴀʀᴄʜ ᴍᴏᴅᴇ", callback_data="SEARCHANSWER"),
            InlineKeyboardButton(text=d, callback_data="CHANGEMODE"),
        ],
        [
            InlineKeyboardButton(text="📡  ᴄʜᴀᴛ ᴛʏᴘᴇ", callback_data="AUTHANSWER"),
            InlineKeyboardButton(text=g, callback_data="CHANNELMODE"),
        ],
        [
            InlineKeyboardButton(text="👥  ᴘʟᴀʏ ᴛʏᴘᴇ", callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(text=p, callback_data="CHANGEPLAYTYPE"),
        ],
        [
            InlineKeyboardButton(text="◁  ʙᴀᴄᴋ", callback_data="settings_helper"),
            InlineKeyboardButton(text="✦  ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    return buttons
