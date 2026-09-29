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

    async def download(
        self, video_id: str, is_live: bool = False, video: bool = False
    ) -> Optional[str]:
        if not yt_dlp:
            logger.error("yt-dlp not installed")
            return None
        if not video_id:
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
            "geo_bypass": True,
            "nocheckcertificate": True,
            "retries": 3,
        }
        try:
            cookie = self._cookies.get_cookies()
        except Exception:
            cookie = None
        if cookie:
            opts["cookiefile"] = cookie

        if video:
            opts["format"] = "best[height<=480][ext=mp4]/best[height<=480]/bestaudio/best"
        else:
            opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
            opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "192",
                }
            ]

        url = f"https://www.youtube.com/watch?v={video_id}"

        def _run():
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            return self._storage.locate_download_file(video_id, video=video)

        try:
            path = await asyncio.to_thread(_run)
            if path:
                return path
        except Exception as e:
            logger.error(f"Download failed for {video_id}: {e}")

        # Fallback without postprocessor
        try:
            opts.pop("postprocessors", None)
            opts["format"] = "bestaudio/best"

            def _run2():
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                return self._storage.locate_download_file(video_id, video=video)

            return await asyncio.to_thread(_run2)
        except Exception as e2:
            logger.error(f"Download fallback failed for {video_id}: {e2}")
            return None
