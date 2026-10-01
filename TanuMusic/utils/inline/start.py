from typing import Union

from pyrogram.types import InlineKeyboardButton

import config
from TanuMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="🟣  ᴀᴅᴅ ᴛᴏ ɢʀᴏᴜᴘ",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text="💬  sᴜᴘᴘᴏʀᴛ",
                url=config.SUPPORT_CHAT,
            ),
        ],
        [
            InlineKeyboardButton(
                text="📢  ᴄʜᴀɴɴᴇʟ",
                url=config.SUPPORT_CHANNEL,
            ),
            InlineKeyboardButton(
                text="👑  ᴏᴡɴᴇʀ",
                url=f"https://t.me/{(config.OWNER_USERNAME or 'KARTIK_NISHAD_3').lstrip('@')}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="✦  ᴄʟᴏsᴇ",
                callback_data="close",
            ),
        ],
    ]
    return buttons


def private_panel(_, BOT_USERNAME=None, OWNER: Union[bool, int] = None):
    uname = BOT_USERNAME or getattr(app, "username", None) or config.BOT_USERNAME or ""
    uname = str(uname).lstrip("@")
    owner = (config.OWNER_USERNAME or "KARTIK_NISHAD_3").lstrip("@")
    buttons = [
        [
            InlineKeyboardButton(
                text="✨  ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  ✨",
                url=f"https://t.me/{uname}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️  ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs",
                callback_data="settings_back_helper",
            ),
            InlineKeyboardButton(
                text="📢  ᴄʜᴀɴɴᴇʟ",
                url=config.SUPPORT_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                text="💬  sᴜᴘᴘᴏʀᴛ",
                url=config.SUPPORT_CHAT,
            ),
            InlineKeyboardButton(
                text="👑  ᴏᴡɴᴇʀ",
                url=f"https://t.me/{owner}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="💎  sᴏᴜʀᴄᴇ",
                url=config.UPSTREAM_REPO or "https://github.com/Kartiknishad36/Tanu_music",
            ),
            InlineKeyboardButton(
                text="🗑  ᴄʟᴏsᴇ",
                callback_data="close",
            ),
        ],
    ]
    return buttons
