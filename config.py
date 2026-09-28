import os
from os import getenv
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID: int = int(getenv("API_ID", "0"))
        self.API_HASH: str = getenv("API_HASH", "")
        self.BOT_TOKEN: str = getenv("BOT_TOKEN", "")
        self.LOGGER_ID: int = int(getenv("LOGGER_ID", "0"))
        self.OWNER_ID: int = int(getenv("OWNER_ID", "0"))
        self.MONGO_DB_URI: str = getenv("MONGO_DB_URI", "")
        self.SESSION1: str = getenv("STRING_SESSION", "")
        self.SESSION2: str = getenv("STRING_SESSION2", "")
        self.SESSION3: str = getenv("STRING_SESSION3", "")
        self.SUPPORT_CHANNEL: str = getenv("SUPPORT_CHANNEL", "https://t.me/ye_duniya_ek_sapna_he")
        self.SUPPORT_CHAT: str = getenv("SUPPORT_CHAT", "https://t.me/+M5ApQJTxdxgxMDg1")
        self.OWNER_USERNAME: str = getenv("OWNER_USERNAME", "KARTIK_NISHAD_3").lstrip("@")
        self.EXCLUDED_CHATS: List[int] = self._parse_excluded_chats()
        self.QUEUE_END_MESSAGE: bool = self._str_to_bool(getenv("QUEUE_END_MESSAGE", "False"))
        self.AUTO_LEAVE: bool = self._str_to_bool(getenv("AUTO_LEAVE", "False"))
        self.THUMB_GEN: bool = self._str_to_bool(getenv("THUMB_GEN", "True"))
        self.VIDEO_MAX_HEIGHT: int = self._parse_video_height()
        self.COOKIES_URL: List[str] = self._parse_cookies()
        self.DEFAULT_THUMB: str = getenv("DEFAULT_THUMB", "")
        self.PING_IMG: str = getenv("PING_IMG", "")
        self.START_IMG: str = getenv("START_IMG", "")
        self.RADIO_IMG: str = getenv("RADIO_IMG", "")
        self.BOT_NAME: str = getenv("BOT_NAME", "Tanu Music")
        self.EXCLUDED_USERNAMES: List[str] = getenv("EXCLUDED_USERNAMES", "").split()

    def _parse_video_height(self) -> int:
        default_height = 480
        raw_value = getenv("VIDEO_MAX_HEIGHT", str(default_height))
        try:
            height = int(raw_value)
        except (TypeError, ValueError):
            return default_height
        if height <= 0:
            return 0
        return max(360, min(height, 1080))

    def _parse_excluded_chats(self) -> List[int]:
        excluded = getenv("EXCLUDED_CHATS", "")
        if not excluded:
            return []
        chat_ids = []
        for chat_id in excluded.split(","):
            chat_id = chat_id.strip()
            if chat_id.lstrip('-').isdigit():
                chat_ids.append(int(chat_id))
        return chat_ids

    def _parse_cookies(self) -> List[str]:
        cookie_str = getenv("COOKIE_URL", "")
        if not cookie_str:
            return []
        return [u.strip() for u in cookie_str.split() if u.strip()]

    def _str_to_bool(self, val: str) -> bool:
        return str(val).lower() in ("1", "true", "yes", "on")

    def check(self):
        missing = []
        if not self.API_ID:
            missing.append("API_ID")
        if not self.API_HASH:
            missing.append("API_HASH")
        if not self.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not self.SESSION1 and not self.SESSION2 and not self.SESSION3:
            missing.append("STRING_SESSION")
        if not self.MONGO_DB_URI:
            missing.append("MONGO_DB_URI")
        if missing:
            raise SystemExit(f"Missing required env: {', '.join(missing)}")
