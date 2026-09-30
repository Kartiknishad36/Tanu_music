import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_USERNAME = getenv("OWNER_USERNAME", "KARTIK_NISHAD_3")
BOT_USERNAME = getenv("BOT_USERNAME", "")
BOT_NAME = getenv("BOT_NAME", "Tanu Music")
ASSUSERNAME = getenv("ASSUSERNAME", "")
LOGGER_ID = int(getenv("LOGGER_ID", "0"))
OWNER_ID = int(getenv("OWNER_ID", "0"))

# Database
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Duration / limits
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "300"))
DURATION_LIMIT = DURATION_LIMIT_MIN * 60
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "180"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "180"))

# Spotify (optional)
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)

# Heroku (optional)
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Kartiknishad36/Tanu_music")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/ye_duniya_ek_sapna_he")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+M5ApQJTxdxgxMDg1")

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "5400"))
AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", "True")

# FIX - yehi missing tha
autoclean = getenv("AUTOCLEAN", "True")
AUTO_SUGGESTION_MODE = getenv("AUTO_SUGGESTION_MODE", "True")
AUTO_SUGGESTION_TIME = int(getenv("AUTO_SUGGESTION_TIME", "5400"))

PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", None)
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://telegra.ph/file/2a7e32a5c1c0c0b0e0c0e.jpg")
START_IMG_URL = getenv("START_IMG_URL", YOUTUBE_IMG_URL)
PING_IMG_URL = getenv("PING_IMG_URL", YOUTUBE_IMG_URL)
PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", YOUTUBE_IMG_URL)
STATS_IMG_URL = getenv("STATS_IMG_URL", YOUTUBE_IMG_URL)
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", YOUTUBE_IMG_URL)
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", YOUTUBE_IMG_URL)
STREAM_IMG_URL = getenv("STREAM_IMG_URL", YOUTUBE_IMG_URL)
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", YOUTUBE_IMG_URL)
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", YOUTUBE_IMG_URL)
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", YOUTUBE_IMG_URL)
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", YOUTUBE_IMG_URL)

# Limits
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
AYU = []
votemode = {}
autoclean = {}
confirm = {}
chatstats = {}
userstats = {}
clean = {}
autoclean = []

COOKIE_URL = getenv("COOKIE_URL", "")

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL url is wrong.")
if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit("[ERROR] - Your SUPPORT_CHAT url is wrong.")
