import re
from typing import Union
from pyrogram import enums, types

class YouTubeUtils:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|live/|embed/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )
        self.stream_regex = re.compile(
            r"https?://[^\s]+\.(?:m3u8|mpd|ts)(\?[^\s]*)?"
            r"|https?://[^\s]*/(?:stream|live|hls|dash)[^\s]*",
            re.IGNORECASE,
        )

    def is_direct_stream(self, url: str) -> bool:
        return bool(re.match(self.stream_regex, url))

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url)) or self.is_direct_stream(url)

    def url(self, message_1: types.Message) -> Union[str, None]:
        messages = [message_1]
        link = None
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            text = message.text or message.caption or ""

            if message.entities:
                for entity in message.entities:
                    if entity.type == enums.MessageEntityType.URL:
                        link = text[entity.offset : entity.offset + entity.length]
                        break

            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == enums.MessageEntityType.TEXT_LINK:
                        link = entity.url
                        break

        if link:
            return link.split("&si")[0].split("?si")[0]
        return None
