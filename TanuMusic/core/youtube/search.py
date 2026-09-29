import asyncio
from typing import Optional, List

from TanuMusic import logger
from TanuMusic.helpers import Track

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Searcher:
    def __init__(self, cookies):
        self._cookies = cookies

    def _ydl_opts(self) -> dict:
        opts = {
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "default_search": "ytsearch",
            "skip_download": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
        }
        # Only set cookiefile when a real path exists
        try:
            cookie = self._cookies.get_cookies() if self._cookies else None
        except Exception:
            cookie = None
        if cookie:
            opts["cookiefile"] = cookie
        return opts

    async def search(self, query: str, m_id: int, music: bool = False) -> Optional[Track]:
        if not yt_dlp:
            logger.error("yt-dlp not installed")
            return None

        q = (query or "").strip()
        if not q:
            return None

        # Text search: force ytsearch1 so we always get a video id
        if not q.startswith("http://") and not q.startswith("https://"):
            if music and "audio" not in q.lower():
                q = f"{q} official audio"
            search_q = f"ytsearch1:{q}"
        else:
            search_q = q

        def _run():
            with yt_dlp.YoutubeDL(self._ydl_opts()) as ydl:
                return ydl.extract_info(search_q, download=False)

        try:
            info = await asyncio.to_thread(_run)
        except Exception as e:
            logger.error(f"YouTube search failed for '{query}': {e}")
            # Retry once without cookies
            try:

                def _run2():
                    opts = {
                        "quiet": True,
                        "no_warnings": True,
                        "noplaylist": True,
                        "default_search": "ytsearch",
                        "skip_download": True,
                        "geo_bypass": True,
                    }
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        return ydl.extract_info(search_q, download=False)

                info = await asyncio.to_thread(_run2)
            except Exception as e2:
                logger.error(f"YouTube search retry failed: {e2}")
                return None

        if not info:
            return None

        if "entries" in info:
            entries = [e for e in (info.get("entries") or []) if e]
            if not entries:
                return None
            info = entries[0]

        vid = info.get("id") or ""
        if not vid:
            return None

        title = info.get("title") or query
        duration = int(info.get("duration") or 0)
        url = info.get("webpage_url") or f"https://www.youtube.com/watch?v={vid}"
        thumbs = info.get("thumbnails") or []
        thumb = ""
        if thumbs:
            thumb = thumbs[-1].get("url", "") or ""
        elif info.get("thumbnail"):
            thumb = info.get("thumbnail")

        from TanuMusic.helpers import utils as u

        return Track(
            id=vid,
            channel_name=info.get("uploader") or info.get("channel") or "YouTube",
            duration=u.format_duration(duration) if duration else "LIVE",
            duration_sec=duration,
            title=title,
            url=url,
            thumbnail=thumb.split("?")[0] if thumb else "",
            view_count=str(info.get("view_count") or ""),
            is_live=bool(info.get("is_live")),
            message_id=m_id,
        )

    async def playlist(self, limit: int, user: str, url: str) -> List[Track]:
        if not yt_dlp:
            return []

        def _run():
            opts = self._ydl_opts()
            opts["extract_flat"] = "in_playlist"
            opts.pop("noplaylist", None)
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)

        try:
            plist = await asyncio.to_thread(_run)
        except Exception as e:
            logger.error(f"Playlist extract failed: {e}")
            return []

        if not plist or not plist.get("entries"):
            return []

        from TanuMusic.helpers import utils as u

        tracks = []
        for data in (plist.get("entries") or [])[:limit]:
            if not data:
                continue
            try:
                duration_sec = int(data.get("duration") or 0)
                tracks.append(
                    Track(
                        id=data.get("id") or "",
                        channel_name=data.get("uploader") or data.get("channel") or "",
                        duration=u.format_duration(duration_sec) if duration_sec else "0:00",
                        duration_sec=duration_sec,
                        title=(data.get("title") or "Unknown")[:80],
                        url=data.get("url")
                        or data.get("webpage_url")
                        or f"https://youtube.com/watch?v={data.get('id')}",
                        user=user,
                        thumbnail="",
                        view_count="",
                    )
                )
            except Exception:
                continue
        return tracks
