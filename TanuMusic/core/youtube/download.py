import asyncio
import os
from typing import Optional

from TanuMusic import logger
from TanuMusic.core.youtube.ydl_opts import download_opts, base_opts

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Downloader:
    def __init__(self, cookies, storage, searcher):
        self._cookies = cookies
        self._storage = storage
        self._searcher = searcher

    def _cookie(self) -> Optional[str]:
        try:
            return self._cookies.get_cookies()
        except Exception:
            return None

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
        url = f"https://www.youtube.com/watch?v={video_id}"
        cookie = self._cookie()

        attempts = []

        # 1) Full opts + cookies + android clients
        attempts.append(download_opts(cookie, video=video, outtmpl=outtmpl))

        # 2) No cookies, android/ios only
        opts2 = base_opts(None, download=True)
        opts2["outtmpl"] = outtmpl
        opts2["extractor_args"] = {
            "youtube": {"player_client": ["android", "ios", "tv_embedded"]}
        }
        if video:
            opts2["format"] = "best[height<=480]/bestaudio/best"
        else:
            opts2["format"] = "bestaudio/best"
        attempts.append(opts2)

        # 3) Minimal — no postprocessor
        opts3 = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": outtmpl,
            "noplaylist": True,
            "format": "bestaudio/best" if not video else "best[height<=480]/best",
            "extractor_args": {
                "youtube": {"player_client": ["android"]}
            },
        }
        if cookie:
            opts3["cookiefile"] = cookie
        attempts.append(opts3)

        last_err = None
        for i, opts in enumerate(attempts, 1):

            def _run(o=opts):
                with yt_dlp.YoutubeDL(o) as ydl:
                    ydl.download([url])
                return self._storage.locate_download_file(video_id, video=video)

            try:
                path = await asyncio.to_thread(_run)
                if path and os.path.exists(path) and os.path.getsize(path) > 0:
                    logger.info(f"Download ok (attempt {i}): {video_id} -> {path}")
                    return path
            except Exception as e:
                last_err = e
                logger.error(f"Download attempt {i} failed for {video_id}: {e}")

        logger.error(f"All download attempts failed for {video_id}: {last_err}")
        return None
