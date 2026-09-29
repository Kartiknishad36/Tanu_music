import asyncio
import os
import re
from typing import Union

import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from TanuMusic.utils.database import is_on_off
from TanuMusic.utils.formatters import time_to_seconds


def _cookies_file() -> str:
    for path in (
        "cookies/cookies.txt",
        "TanuMusic/cookies/cookies.txt",
        "cookies.txt",
        "TanuMusic/assets/Cookies.txt",
    ):
        if os.path.exists(path):
            return path
    return "cookies/cookies.txt"


def _ydl_base(extra=None):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "cookiefile": _cookies_file(),
        "extractor_args": {"youtube": {"player_client": ["android", "ios", "tv_embedded"]}},
    }
    if extra:
        opts.update(extra)
    return opts


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption or ""
                        return text[entity.offset : entity.offset + entity.length]
            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            return result["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies",
            _cookies_file(),
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download --cookies {_cookies_file()} {link}"
        )
        try:
            result = playlist.split("\n")
            result = [r for r in result if r]
        except Exception:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ydl = yt_dlp.YoutubeDL(_ydl_base())
        with ydl:
            formats_available = []
            r = ydl.extract_info(link, download=False)
            for format in r["formats"]:
                try:
                    str(format["format"])
                except Exception:
                    continue
                if not format.get("filesize") and not format.get("filesize_approx"):
                    continue
                formats_available.append(
                    {
                        "format": format["format"],
                        "filesize": format.get("filesize") or format.get("filesize_approx"),
                        "format_id": format["format_id"],
                        "ext": format["ext"],
                        "format_note": format.get("format_note"),
                        "yturl": link,
                    }
                )
        return formats_available, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_opts = _ydl_base(
                {
                    "format": "bestaudio/best",
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "prefer_ffmpeg": True,
                }
            )
            x = yt_dlp.YoutubeDL(ydl_opts)
            info = x.extract_info(link, download=False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_opts = _ydl_base(
                {
                    "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                    "outtmpl": "downloads/%(id)s.%(ext)s",
                    "prefer_ffmpeg": True,
                    "merge_output_format": "mp4",
                }
            )
            x = yt_dlp.YoutubeDL(ydl_opts)
            info = x.extract_info(link, download=False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        if songvideo:
            ydl_opts = _ydl_base(
                {
                    "format": f"{format_id}+bestaudio",
                    "outtmpl": f"downloads/{title}.%(ext)s",
                    "prefer_ffmpeg": True,
                    "merge_output_format": "mp4",
                }
            )
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link]))
            return f"downloads/{title}.mp4"
        elif songaudio:
            ydl_opts = _ydl_base(
                {
                    "format": format_id,
                    "outtmpl": f"downloads/{title}.%(ext)s",
                    "prefer_ffmpeg": True,
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link]))
            return f"downloads/{title}.mp3"
        elif video:
            if await is_on_off(1):
                downloaded_file = await loop.run_in_executor(None, video_dl)
                direct = True
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp",
                    "--cookies",
                    _cookies_file(),
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    f"{link}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, _stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = None
                else:
                    return
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct


async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        err = errorz.decode("utf-8")
        if "unavailable videos are hidden" in err.lower():
            return out.decode("utf-8")
        return err
    return out.decode("utf-8")
