from os import getenv
from typing import List
from dotenv import load_dotenv

load_dotenv()

_DEFAULT_START = "https://telegra.ph/file/2a7e32a5c1c0c0b0e0c0e.jpg"
_DEFAULT_PING = "https://telegra.ph/file/2a7e32a5c1c0c0b0e0c0e.jpg"


class Config:
    def __init__(self):
        self.API_ID: int = int(getenv("API_ID", "0"))
        self.API_HASH: str = getenv("API_HASH", "")

        self.BOT_TOKEN: str = getenv("BOT_TOKEN", "")
        self.BOT_USERNAME: str = getenv("BOT_USERNAME", "").lstrip("@")
        self.BOT_NAME: str = getenv("BOT_NAME", "Tanu Music")
        # Hardcoded log group
        self.LOGGER_ID: int = int(getenv("LOGGER_ID", "-1004445549766") or "-1004445549766")
        self.OWNER_ID: int = int(getenv("OWNER_ID", "0"))

        self.MONGO_URL: str = getenv("MONGO_DB_URI", "")

        self.DURATION_LIMIT: int = int(getenv("DURATION_LIMIT", "300")) * 60
        self.QUEUE_LIMIT: int = int(getenv("QUEUE_LIMIT", "30"))
        self.PLAYLIST_LIMIT: int = int(getenv("PLAYLIST_LIMIT", "20"))
        self.PLAYLIST_MAX: int = int(getenv("PLAYLIST_MAX", "60"))

        self.SPOTIFY_CLIENT_ID: str = getenv("SPOTIFY_CLIENT_ID") or getenv("SPOTIPY_CLIENT_ID", "")
        self.SPOTIFY_CLIENT_SECRET: str = getenv("SPOTIFY_CLIENT_SECRET") or getenv(
            "SPOTIPY_CLIENT_SECRET", ""
        )

        self.SESSION1: str = getenv("STRING_SESSION", "")
        self.SESSION2: str = getenv("STRING_SESSION2", "")
        self.SESSION3: str = getenv("STRING_SESSION3", "")

        self.SUPPORT_CHANNEL: str = getenv(
            "SUPPORT_CHANNEL", "https://t.me/ye_duniya_ek_sapna_he"
        )
        self.SUPPORT_CHAT: str = getenv(
            "SUPPORT_CHAT", "https://t.me/+M5ApQJTxdxgxMDg1"
        )
        self.OWNER_USERNAME: str = getenv("OWNER_USERNAME", "KARTIK_NISHAD_3").lstrip("@")

        self.EXCLUDED_CHATS: List[int] = self._parse_excluded_chats()

        self.QUEUE_END_MESSAGE: bool = self._str_to_bool(
            getenv("QUEUE_END_MESSAGE", "False")
        )
        self.AUTO_LEAVE: bool = self._str_to_bool(getenv("AUTO_LEAVE", "False"))

        self.VIDEO_MAX_HEIGHT: int = self._parse_video_height()

        self.COOKIES_URL: List[str] = self._parse_cookies()

        self.DEFAULT_THUMB: str = getenv("DEFAULT_THUMB", "") or _DEFAULT_START
        self.PING_IMG: str = getenv("PING_IMG", "") or _DEFAULT_PING
        self.START_IMG: str = getenv("START_IMG", "") or _DEFAULT_START
        self.RADIO_IMG: str = getenv("RADIO_IMG", "") or _DEFAULT_START

        self.EXCLUDED_USERNAMES: List[str] = [
            x.strip() for x in getenv("EXCLUDED_USERNAMES", "").split() if x.strip()
        ]

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
            if chat_id.lstrip("-").isdigit():
                chat_ids.append(int(chat_id))
        return chat_ids

    def _parse_cookies(self) -> List[str]:
        cookie_str = getenv("COOKIE_URL", "")
        if not cookie_str:
            return []
        valid_sources = ["batbin.me", "pastebin.com", "paste.ee", "rentry.co"]
        return [
            url.strip()
            for url in cookie_str.split()
            if url.strip() and any(source in url for source in valid_sources)
        ]

    @staticmethod
    def _str_to_bool(value: str) -> bool:
        return value.lower() in ("true", "1", "yes", "y", "on")

    def check(self) -> None:
        required_vars = {
            "API_ID": self.API_ID,
            "API_HASH": self.API_HASH,
            "BOT_TOKEN": self.BOT_TOKEN,
            "MONGO_DB_URI": self.MONGO_URL,
            "LOGGER_ID": self.LOGGER_ID,
            "OWNER_ID": self.OWNER_ID,
            "STRING_SESSION": self.SESSION1,
        }
        missing = [
            name
            for name, value in required_vars.items()
            if not value or (isinstance(value, int) and value == 0)
        ]
        if missing:
            raise SystemExit(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Set them in Railway Variables / .env"
            )
