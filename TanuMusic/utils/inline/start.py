from typing import Union

from pyrogram.types import InlineKeyboardButton

import config
from TanuMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_3"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_, BOT_USERNAME=None, OWNER: Union[bool, int] = None):
    uname = BOT_USERNAME or getattr(app, "username", None) or config.BOT_USERNAME or ""
    uname = str(uname).lstrip("@")
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{uname}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_8"], callback_data="settings_back_helper"),
            InlineKeyboardButton(text=_["S_B_1"], url=f"https://t.me/{uname}?start=help"),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{(config.OWNER_USERNAME or 'KARTIK_NISHAD_3').lstrip('@')}",
            ),
            InlineKeyboardButton(
                text=_["S_B_6"] if "S_B_6" in _ else "Source",
                url=config.UPSTREAM_REPO or "https://github.com/Kartiknishad36/Tanu_music",
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"] if "CLOSE_BUTTON" in _ else "Close", callback_data="close"),
        ],
    ]
    return buttons
