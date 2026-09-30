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
        dest = getattr(config, "DOWNLOADS_DEST", "downloads")
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)

        if audio:
            try:
                ext = "ogg"
                if audio.file_name and "." in audio.file_name:
                    raw_ext = audio.file_name.split(".")[-1]
                    if raw_ext not in ["opus", "m4a", "webm"]:
                        ext = raw_ext
                file_name = f"{audio.file_unique_id}.{ext}"
            except Exception:
                file_name = f"{audio.file_unique_id}.ogg"
            return os.path.join(dest, file_name)

        if video:
            try:
                ext = "mp4"
                if video.file_name and "." in video.file_name:
                    ext = video.file_name.split(".")[-1]
                file_name = f"{video.file_unique_id}.{ext}"
            except Exception:
                file_name = f"{video.file_unique_id}.mp4"
            return os.path.join(dest, file_name)

        return os.path.join(dest, "telegram_file")

    async def download(self, message, mystic, fname: str):
        try:
            async def progress(current, total):
                if total == 0:
                    return
                try:
                    percentage = current * 100 / total
                    if current % (5 * 1024 * 1024) == 0 or current == total:
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
            try:
                await mystic.edit_text(f"Download failed: {e}")
            except Exception:
                pass
            return False
