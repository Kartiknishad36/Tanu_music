import asyncio
import importlib
import sys
from pyrogram import idle

from TanuMusic import config, logger, tasks, boot
from TanuMusic.core.bot import Bot
from TanuMusic.core.userbot import Userbot
from TanuMusic.core.mongo import MongoDB
from TanuMusic.core.lang import Language
from TanuMusic.core.dir import ensure_dirs
from TanuMusic.core.telegram import Telegram
from TanuMusic.core.youtube import YouTube
from TanuMusic.core.spotify import Spotify
from TanuMusic.core.preload import PreloadManager
from TanuMusic.helpers import Queue
from TanuMusic.core.calls import TgCall
import TanuMusic

# --- Core Init (circular free) ---
ensure_dirs()
app = Bot()
userbot = Userbot()
db = MongoDB()
lang = Language()
tg = Telegram()
yt = YouTube()
spotify = Spotify()
queue = Queue()
tune = TgCall()
preload = PreloadManager()

# Baaki purani files `from TanuMusic import app` kar sake isliye inject kar do
TanuMusic.app = app
TanuMusic.userbot = userbot
TanuMusic.db = db
TanuMusic.lang = lang
TanuMusic.tg = tg
TanuMusic.yt = yt
TanuMusic.spotify = spotify
TanuMusic.queue = queue
TanuMusic.tune = tune
TanuMusic.preload = preload
TanuMusic.config = config
TanuMusic.logger = logger

async def main():
    await db.connect()
    
    await app.boot()
    await userbot.boot()
    await tune.boot()
    
    # Load plugins
    from TanuMusic.core.plugins import load_plugins
    await load_plugins()

    logger.info("TanuMusic Started Successfully!")
    await idle()

    await TanuMusic.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
