from pyrogram import types

from TanuMusic import app, config


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
        is_playing: bool = True,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append(
                [self.ikb(text=status, callback_data=f"controls status {chat_id}")]
            )
        elif timer:
            keyboard.append(
                [self.ikb(text=timer, callback_data=f"controls status {chat_id}")]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="« 30", callback_data=f"controls seek_back_30 {chat_id}"),
                    self.ikb(text="« 10", callback_data=f"controls seek_back_10 {chat_id}"),
                    self.ikb(text="10 »", callback_data=f"controls seek_forward_10 {chat_id}"),
                    self.ikb(text="30 »", callback_data=f"controls seek_forward_30 {chat_id}"),
                ]
            )
            keyboard.append(
                [
                    self.ikb(
                        text="II" if is_playing else "▷",
                        callback_data=f"controls {'pause' if is_playing else 'resume'} {chat_id}",
                    ),
                    self.ikb(text="I◁", callback_data=f"controls previous {chat_id}"),
                    self.ikb(text="↻", callback_data=f"controls replay {chat_id}"),
                    self.ikb(text="▷I", callback_data=f"controls skip {chat_id}"),
                    self.ikb(text="▢", callback_data=f"controls stop {chat_id}"),
                ]
            )
            keyboard.append(
                [self.ikb(text="ᴅᴇʟᴇᴛᴇ", callback_data=f"controls close {chat_id}")]
            )

        return self.ikm(keyboard)

    def queue_markup(self, chat_id: int, _text: str, playing: bool) -> types.InlineKeyboardMarkup:
        action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(text=_text, callback_data=f"controls {action} {chat_id} q")]]
        )

    def settings_markup(
        self, lang: dict, admin_only: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        mode = lang.get("play_mode", "Play Mode")
        label = "Admins" if admin_only else "Everyone"
        return self.ikm(
            [
                [
                    self.ikb(text=f"{mode} ➜", callback_data=f"controls status {chat_id}"),
                    self.ikb(text=label, callback_data="playmode"),
                ],
            ]
        )

    def start_key(self, lang: dict, private: bool = False) -> types.InlineKeyboardMarkup:
        uname = getattr(app, "username", None) or config.BOT_USERNAME or ""
        uname = str(uname).lstrip("@")
        add_url = f"https://t.me/{uname}?startgroup=true" if uname else config.SUPPORT_CHAT

        rows = [
            [self.ikb(text=lang.get("add_me", "➕ Add me to your group"), url=add_url)],
            [self.ikb(text=lang.get("help", "📖 Help"), callback_data="help")],
            [
                self.ikb(
                    text=lang.get("support", "💬 Support"),
                    url=config.SUPPORT_CHAT or "https://t.me/KARTIK_NISHAD_3",
                ),
                self.ikb(
                    text=lang.get("channel", "📢 Channel"),
                    url=config.SUPPORT_CHANNEL or "https://t.me/ye_duniya_ek_sapna_he",
                ),
            ],
            [
                self.ikb(
                    text=lang.get("owner", "👤 Owner"),
                    url=f"https://t.me/{(config.OWNER_USERNAME or 'KARTIK_NISHAD_3').lstrip('@')}",
                )
            ],
        ]
        if private:
            rows.append(
                [
                    self.ikb(
                        text=lang.get("source", "🛠 Source"),
                        url="https://github.com/Kartiknishad36/Tanu_music",
                    )
                ]
            )
        return self.ikm(rows)

    def help_markup(self, lang: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="🎵 Play", callback_data="help_play"),
                    self.ikb(text="✨ Extra", callback_data="help_extra"),
                ],
                [
                    self.ikb(text="🛡 Admin", callback_data="help_admin"),
                    self.ikb(text="🔧 Tools", callback_data="help_tools"),
                ],
                [
                    self.ikb(text="👑 Sudo", callback_data="help_sudo"),
                    self.ikb(text="📻 Radio", callback_data="help_radio"),
                ],
                [self.ikb(text=lang.get("close", "Close"), callback_data="controls close 0")],
            ]
        )

    def ping_markup(self, support_text: str = "Support") -> types.InlineKeyboardMarkup:
        rows = []
        if config.SUPPORT_CHAT:
            rows.append([self.ikb(text=support_text, url=config.SUPPORT_CHAT)])
        if config.SUPPORT_CHANNEL:
            rows.append([self.ikb(text="Updates", url=config.SUPPORT_CHANNEL)])
        if not rows:
            rows = [[self.ikb(text="Owner", url="https://t.me/KARTIK_NISHAD_3")]]
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [[self.ikb(text="ᴏᴘᴇɴ ɪɴ ʏᴏᴜᴛᴜʙᴇ", url=link)]]
        )

    def radio_markup(self) -> types.InlineKeyboardMarkup:
        rows = []
        row = []
        for i, key in enumerate(["lofi", "pop", "dance", "rock", "jazz"]):
            row.append(self.ikb(text=key.title(), callback_data=f"radio_{key}"))
            if len(row) == 3:
                rows.append(row)
                row = []
        if row:
            rows.append(row)
        return self.ikm(rows)
