from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TanuMusic import config


class Inline:
    def controls(self, chat_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸", callback_data=f"pause_{chat_id}"),
                    InlineKeyboardButton("▶️", callback_data=f"resume_{chat_id}"),
                    InlineKeyboardButton("⏭", callback_data=f"skip_{chat_id}"),
                    InlineKeyboardButton("⏹", callback_data=f"stop_{chat_id}"),
                ]
            ]
        )

    def queue_markup(self, chat_id: int, status: str, playing: bool) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(status, callback_data="noop")],
                [
                    InlineKeyboardButton("⏭ Skip", callback_data=f"skip_{chat_id}"),
                    InlineKeyboardButton("⏹ Stop", callback_data=f"stop_{chat_id}"),
                ],
            ]
        )

    def ping_markup(self, support_text: str) -> InlineKeyboardMarkup:
        rows = []
        if config.SUPPORT_CHAT:
            rows.append([InlineKeyboardButton(support_text or "Support", url=config.SUPPORT_CHAT)])
        if config.SUPPORT_CHANNEL:
            rows.append([InlineKeyboardButton("Updates", url=config.SUPPORT_CHANNEL)])
        return InlineKeyboardMarkup(rows or [[InlineKeyboardButton("Tanu Music", url="https://t.me/KARTIK_NISHAD_3")]])

    def start_key(self, lang, private: bool) -> InlineKeyboardMarkup:
        rows = []
        uname = (config.BOT_USERNAME or "").lstrip("@")
        if uname:
            rows.append([
                InlineKeyboardButton(
                    "➕ Add to Group",
                    url=f"https://t.me/{uname}?startgroup=true",
                )
            ])
        if config.SUPPORT_CHAT:
            rows.append([InlineKeyboardButton("Support", url=config.SUPPORT_CHAT)])
        if config.SUPPORT_CHANNEL:
            rows.append([InlineKeyboardButton("Channel", url=config.SUPPORT_CHANNEL)])
        owner = config.OWNER_USERNAME or "KARTIK_NISHAD_3"
        rows.append([InlineKeyboardButton("Owner", url=f"https://t.me/{owner.lstrip('@')}")])
        return InlineKeyboardMarkup(rows)

    def help_markup(self, lang) -> InlineKeyboardMarkup:
        return self.start_key(lang, True)

    def settings_markup(self, lang, admin_only, language, chat_id) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Admin only: ON" if admin_only else "Admin only: OFF",
                        callback_data=f"playmode_{chat_id}",
                    )
                ],
                [InlineKeyboardButton("Language", callback_data=f"langmenu_{chat_id}")],
            ]
        )
