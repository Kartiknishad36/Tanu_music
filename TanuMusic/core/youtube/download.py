import asyncio
import os
from typing import Optional
from TanuMusic import logger

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Downloader:
    def __init__(self, cookies, storage, searcher):
        self._cookies = cookies
        self._storage = storage
        self._searcher = searcher

    async def download(self, video_id: str, is_live: bool = False, video: bool = False) -> Optional[str]:
        if not yt_dlp:
            logger.error("yt-dlp not installed")
            return None

        cached = self._storage.locate_download_file(video_id, video=video)
        if cached:
            return cached

        os.makedirs("downloads", exist_ok=True)
        outtmpl = f"downloads/{video_id}.%(ext)s"

        opts = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": outtmpl,
            "noplaylist": True,
        }
        cookie = self._cookies.get_cookies()
        if cookie:
            opts["cookiefile"] = cookie

        if video:
            opts["format"] = "best[height<=480]/bestaudio/best"
        else:
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }]

        url = f"https://www.youtube.com/watch?v={video_id}"

        def _run():
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return self._storage.locate_download_file(video_id, video=video)

        try:
            path = await asyncio.to_thread(_run)
            return path
        except Exception as e:
            logger.error(f"Download failed for {video_id}: {e}")
            return None
