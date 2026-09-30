import os
import re

from config import YOUTUBE_IMG_URL

try:
    from youtubesearchpython.__future__ import VideosSearch
except Exception:
    VideosSearch = None


async def gen_thumb(videoid, user_id=None):
    """Return a thumbnail path/URL for a video id. Falls back to default image."""
    try:
        cache_path = f"cache/{videoid}_v4.png"
        if os.path.isfile(cache_path):
            return cache_path
    except Exception:
        pass
    return YOUTUBE_IMG_URL


async def get_thumb(videoid):
    return await gen_thumb(videoid)
