import asyncio
import os
import time
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Voice

import config
from TanuMusic import app
from TanuMusic.utils.formatters import (
    check_duration,
    convert_bytes,
    get_readable_time,
    seconds_to_min,
)


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.time_line = {}

    async def send_split_text(self, message, string):
        n = self.chars_limit
        out = [string[i : i + n] for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x)
        return True

    async def get_link(self, message):
        if message.chat.username:
            return f"https://t.me/{message.chat.username}/{message.reply_to_message.id}"
        return message.link

    async def get_filename(self, file, audio: Union[bool, str] = None):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = "Telegram Audio File" if audio else "Telegram Video File"
        except Exception:
            file_name = "Telegram Audio File" if audio else "Telegram Video File"
        return file_name

    async def get_duration(self, file):
        try:
            dur = seconds_to_min(file.duration)
        except Exception:
            dur = "Unknown"
        return dur

    async def get_filepath(
        self,
        audio: Union[bool, str] = None,
        video: Union[bool, str] = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (
                            audio.file_name.split(".")[-1]
                            if ("." in audio.file_name
and audio.file_name.split(".")[-1]
                            not in ["opus", "m4a", "webm"]
                            else "ogg"
                        )
                        if audio.file_name
                        else "ogg"
                    )
                )
            except Exception:
                file_name = audio.file_unique_id + ".ogg"
            file_path = os.path.join(config.DOWNLOADS_DEST, file_name)
        if video:
            try:
                file_name = (
                    video.file_unique_id
                    + "."
                    + (video.file_name.split(".")[-1] if video.file_name else "mp4")
                )
            except Exception:
                file_name = video.file_unique_id + ".mp4"
            file_path = os.path.join(config.DOWNLOADS_DEST, file_name)
        return file_path

    async def download(self, message, mystic, fname: str):
        try:
            left_time = {}
            speed_counter = {}

            def speed_count(to_download, filename, size):
                if time.time() not in speed_counter:
                    speed_counter[time.time()] = 0
                try:
                    percentage = (to_download / size) * 100
                    speed = (to_download - speed_counter[list(speed_counter.keys())[-1]]) / (
                        time.time() - list(speed_counter.keys())[-1]
                    )
                    remaining = (size - to_download) / speed if speed else 0
                    left_time[filename] = remaining
                except Exception:
                    pass

            async def progress(current, total):
                if current == total:
                    try:
                        speed_counter.clear()
                        left_time.clear()
                    except Exception:
                        pass
                    return
                try:
                    speed_count(current, fname, total)
                    if current % (5 * 1024 * 1024) == 0 or current == total:
                        percentage = current * 100 / total
                        await mystic.edit_text(
                            f"**Downloading...**\n\n"
                            f"• Progress: `{percentage:.1f}%`\n"
                            f"• Downloaded: `{convert_bytes(current)}` / `{convert_bytes(total)}`"
                        )
                except Exception:
                    pass

            if os.path.exists(fname):
                return True
            await app.download_media(
                message.reply_to_message,
                file_name=fname,
                progress=progress,
            )
            return True
        except Exception as e:
            await mystic.edit_text(f"Download failed: {e}")
            return False
