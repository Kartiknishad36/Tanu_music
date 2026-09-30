from TanuMusic.core.bot import BABY
from TanuMusic.core.dir import dirr
from TanuMusic.core.git import git
from TanuMusic.core.userbot import Userbot
from TanuMusic.misc import dbb, heroku, db
from pyrogram import Client

try:
    from SafoneAPI import SafoneAPI
except Exception:
    SafoneAPI = None

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = BABY()
api = SafoneAPI() if SafoneAPI else None
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
