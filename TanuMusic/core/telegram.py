from pyrogram import types
from TanuMusic.helpers import Media
from TanuMusic.helpers import utils as util

class Telegram:
    def get_media(self, message: types.Message | None):
        if not message:
            return None
        return None  # Telegram media play optional in this build

    async def download(self, message: types.Message) -> Media | None:
        return None
