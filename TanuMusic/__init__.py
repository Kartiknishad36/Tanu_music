import asyncio, time, logging
from logging.handlers import RotatingFileHandler
from typing import List
from pyrogram.errors import ChannelInvalid

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[RotatingFileHandler("log.txt", maxBytes=10485760, backupCount=5), logging.StreamHandler()],
    level=logging.INFO,
)
for n in ["httpx","ntgcalls","pymongo","pyrogram","pytgcalls","spotipy","spotipy.client"]:
    logging.getLogger(n).setLevel(logging.ERROR)

logger = logging.getLogger("TanuMusic")

def _asyncio_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, ChannelInvalid):
        logger.warning("Ignoring CHANNEL_INVALID")
        return
    loop.default_exception_handler(context)
asyncio.get_event_loop().set_exception_handler(_asyncio_exception_handler)

__version__ = "3.0.1"

from config import Config
config = Config()
config.check()

tasks: List = []
boot: float = time.time()

# Placeholders taaki `from TanuMusic import userbot` fail na ho
app = None
userbot = None
db = None
lang = None
tg = None
yt = None
spotify = None
queue = None
tune = None
preload = None
