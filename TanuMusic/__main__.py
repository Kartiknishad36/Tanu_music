import asyncio
import importlib
import pathlib
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

def load_plugins():
    count = 0
    for path in pathlib.Path("TanuMusic/plugins").glob("*.py"):
        if path.name.startswith("_"):
            continue
        try:
            importlib.import_module(f"TanuMusic.plugins.{path.stem}")
            count += 1
        except Exception as e:
            logger.error(f"Failed to load {path.stem}: {e}")
    logger.info(f"Loaded {count} plugins")

async def stop():
    logger.info("Stopping bot...")
    for task in tasks:
        task.cancel()
        try:
            await task
        except:
            pass
    try:
        await app.exit()
    except: pass
    try:
        await userbot.exit()
    except: pass
    try:
        await db.close()
    except: pass

async def main():
    await db.connect()
    await lang.load()
    await app.boot()
    await userbot.boot()
    await tune.boot()
    
    load_plugins()

    logger.info("TanuMusic Started Successfully!")
    await idle()
    await stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
