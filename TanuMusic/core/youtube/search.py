import asyncio
from typing import Optional, List

from TanuMusic import logger
from TanuMusic.helpers import Track
from TanuMusic.core.youtube.ydl_opts import search_opts, base_opts

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


class Searcher:
    def __init__(self, cookies):
        self._cookies = cookies

    def _cookie(self) -> Optional[str]:
        try:
            return self._cookies.get_cookies() if self._cookies else None
        except Exception:
            return None

    async def search(self, query: str, m_id: int, music: bool = False) -> Optional[Track]:
        if not yt_dlp:
            logger.error("yt-dlp not installed")
            return None

        q = (query or "").strip()
        if not q:
            return None

        is_url = q.startswith("http://") or q.startswith("https://")
        if not is_url:
            search_q = f"ytsearch1:{q}"
        else:
            search_q = q

        cookie = self._cookie()

        async def _extract(opts: dict):
            def _run():
                with yt_dlp.YoutubeDL(opts) as ydl:
                    return ydl.extract_info(search_q, download=False)

            return await asyncio.to_thread(_run)

        info = None
        errors = []

        # Attempt 1: full opts + cookies
        try:
            info = await _extract(search_opts(cookie))
        except Exception as e:
            errors.append(str(e))
            logger.error(f"YouTube search failed for '{query}': {e}")

        # Attempt 2: android-only, no cookies
        if not info:
            try:
                opts = base_opts(None, download=False)
                opts["extractor_args"] = {
                    "youtube": {"player_client": ["android", "ios"]}
                }
                info = await _extract(opts)
            except Exception as e:
                errors.append(str(e))
                logger.error(f"YouTube search retry failed: {e}")

        # Attempt 3: flat ytsearch (metadata only, no player)
        if not info and not is_url:
            try:
                opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "extract_flat": "in_playlist",
                    "default_search": "ytsearch",
                    "skip_download": True,
                }

                def _flat():
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        return ydl.extract_info(f"ytsearch5:{q}", download=False)

                flat = await asyncio.to_thread(_flat)
                if flat and flat.get("entries"):
                    e0 = next((e for e in flat["entries"] if e), None)
                    if e0 and e0.get("id"):
                        info = {
                            "id": e0["id"],
                            "title": e0.get("title") or q,
                            "duration": e0.get("duration") or 0,
                            "uploader": e0.get("uploader") or "YouTube",
                            "webpage_url": e0.get("url")
                            or f"https://www.youtube.com/watch?v={e0['id']}",
                            "thumbnail": (e0.get("thumbnails") or [{}])[-1].get("url", "")
                            if e0.get("thumbnails")
                            else "",
                            "view_count": e0.get("view_count") or "",
                            "is_live": bool(e0.get("is_live")),
                        }
            except Exception as e:
                errors.append(str(e))
                logger.error(f"Flat search failed: {e}")

        if not info:
            logger.error(f"All search methods failed for '{query}': {errors}")
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
            thumb = info.get("thumbnail") or ""

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

        cookie = self._cookie()

        def _run():
            opts = search_opts(cookie)
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
                        duration=u.format_duration(duration_sec)
                        if duration_sec
                        else "0:00",
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
