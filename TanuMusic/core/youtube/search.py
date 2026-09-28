import asyncio
from typing import Optional, List
from TanuMusic.helpers import Track
from TanuMusic import logger

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Searcher:
    def __init__(self, cookies):
        self._cookies = cookies

    def _ydl_opts(self, flat: bool = True) -> dict:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": flat,
            "default_search": "ytsearch",
        }
        cookie = self._cookies.get_cookies()
        if cookie:
            opts["cookiefile"] = cookie
        return opts

    async def search(self, query: str, m_id: int, music: bool = False) -> Optional[Track]:
        if not yt_dlp:
            logger.error("yt-dlp not installed")
            return None

        def _run():
            q = query if query.startswith("http") else f"ytsearch1:{query}"
            with yt_dlp.YoutubeDL(self._ydl_opts(flat=False)) as ydl:
                info = ydl.extract_info(q, download=False)
            if not info:
                return None
            if "entries" in info:
                entries = [e for e in info["entries"] if e]
                if not entries:
                    return None
                info = entries[0]
            return info

        try:
            info = await asyncio.to_thread(_run)
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
            return None

        if not info:
            return None

        vid = info.get("id") or ""
        title = info.get("title") or query
        duration = int(info.get("duration") or 0)
        url = info.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}"

        from TanuMusic.helpers import utils as u

        return Track(
            id=vid,
            channel_name=info.get("uploader") or "YouTube",
            duration=u.format_duration(duration) if duration else "LIVE",
            duration_sec=duration,
            title=title,
            url=url,
            thumbnail=(info.get("thumbnail") or ""),
            view_count=str(info.get("view_count") or ""),
            is_live=bool(info.get("is_live")),
            message_id=m_id,
        )

    async def playlist(self, limit: int, user: str, url: str) -> List[Track]:
        return []
