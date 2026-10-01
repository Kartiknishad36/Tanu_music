import asyncio
import time
import logging
from logging.handlers import RotatingFileHandler
from typing import List
from pyrogram.errors import ChannelInvalid

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
)

for n in ["httpx", "ntgcalls", "pymongo", "pyrogram", "pytgcalls", "spotipy", "spotipy.client"]:
    logging.getLogger(n).setLevel(logging.ERROR)

logger = logging.getLogger("TanuMusic")


def _asyncio_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, ChannelInvalid):
        logger.warning("Ignoring CHANNEL_INVALID")
        return
    loop.default_exception_handler(context)


try:
    asyncio.get_event_loop().set_exception_handler(_asyncio_exception_handler)
except Exception:
    pass

__version__ = "3.0.1"

from config import Config

config = Config()
config.check()

tasks: List = []
boot: float = time.time()

from TanuMusic.core.dir import ensure_dirs

ensure_dirs()

from TanuMusic.core.bot import Bot

app = Bot()

from TanuMusic.core.userbot import Userbot

userbot = Userbot()

from TanuMusic.core.mongo import MongoDB

db = MongoDB()

from TanuMusic.core.lang import Language

lang = Language()

from TanuMusic.core.telegram import Telegram
from TanuMusic.core.youtube import YouTube
from TanuMusic.core.spotify import Spotify

tg = Telegram()
yt = YouTube()
spotify = Spotify()

from TanuMusic.helpers._queue import Queue

queue = Queue()

from TanuMusic.core.preload import PreloadManager

preload = PreloadManager()

from TanuMusic.core.calls import TgCall

tune = TgCall()


async def stop() -> None:
    logger.info("Stopping bot...")
    for task in list(tasks):
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, Exception):
            pass
    try:
        await app.exit()
    except Exception:
        pass
    try:
        await userbot.exit()
    except Exception:
        pass
    try:
        await db.close()
    except Exception:
        pass
    logger.info("Bot stopped.")
