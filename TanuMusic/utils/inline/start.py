from typing import Union

from pyrogram.types import InlineKeyboardButton

import config
from TanuMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_.get("S_B_1", "➕ Add to Group"),
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(
                text=_.get("S_B_2", "Support"),
                url=config.SUPPORT_CHAT,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_4", "Channel"),
                url=config.SUPPORT_CHANNEL,
            ),
            InlineKeyboardButton(
                text=_.get("S_B_5", "Owner"),
                url=f"https://t.me/{(config.OWNER_USERNAME or 'KARTIK_NISHAD_3').lstrip('@')}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_.get("CLOSE_BUTTON", "Close"),
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
                text=_.get("S_B_3", "➕ Add me to your Group"),
                url=f"https://t.me/{uname}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_8", "⚙️ Help & Commands"),
                callback_data="settings_back_helper",
            ),
            InlineKeyboardButton(
                text=_.get("S_B_1", "📢 Channel"),
                url=config.SUPPORT_CHANNEL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_2", "💬 Support"),
                url=config.SUPPORT_CHAT,
            ),
            InlineKeyboardButton(
                text=_.get("S_B_5", "👤 Owner"),
                url=f"https://t.me/{owner}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_.get("S_B_6", "🧾 Source"),
                url=config.UPSTREAM_REPO or "https://github.com/Kartiknishad36/Tanu_music",
            ),
            InlineKeyboardButton(
                text=_.get("CLOSE_BUTTON", "🗑 Close"),
                callback_data="close",
            ),
        ],
    ]
    return buttons
