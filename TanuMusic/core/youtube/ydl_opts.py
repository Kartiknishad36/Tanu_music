"""Shared yt-dlp options — fixes YouTube 'page needs to be reloaded'."""
from typing import Optional


def base_opts(cookiefile: Optional[str] = None, *, download: bool = False) -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "retries": 5,
        "fragment_retries": 5,
        "ignoreerrors": False,
        # Critical: avoid web player that triggers "page needs to be reloaded"
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "tv_embedded", "mweb"],
                "player_skip": ["webpage", "configs"],
            }
        },
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    }
    if cookiefile:
        opts["cookiefile"] = cookiefile
    if not download:
        opts["skip_download"] = True
        opts["default_search"] = "ytsearch"
    return opts


def search_opts(cookiefile: Optional[str] = None) -> dict:
    opts = base_opts(cookiefile, download=False)
    # Flat search is faster / less blocked for ytsearch
    opts["extract_flat"] = False
    return opts


def download_opts(
    cookiefile: Optional[str] = None,
    *,
    video: bool = False,
    outtmpl: str = "downloads/%(id)s.%(ext)s",
) -> dict:
    opts = base_opts(cookiefile, download=True)
    opts["outtmpl"] = outtmpl
    if video:
        opts["format"] = (
            "best[height<=480][ext=mp4]/"
            "best[height<=480]/"
            "bestaudio/best"
        )
    else:
        # Prefer progressive audio formats android client understands
        opts["format"] = "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ]
    return opts
