import os
from TanuMusic import config
from TanuMusic.helpers._dataclass import Track

class Thumbnail:
    async def generate(self, media) -> str:
        if isinstance(media, Track) and getattr(media, "thumbnail", None):
            return media.thumbnail
        return config.DEFAULT_THUMB or config.START_IMG or config.PING_IMG or ""
