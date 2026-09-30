import re
from pyrogram.types import InlineKeyboardButton

BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))"
)


def button_markdown_parser(text):
    markdown_note = text
    text_data = ""
    buttons = []
    if markdown_note is None:
        return text_data, buttons
    if markdown_note.startswith("/"):
        args = markdown_note.split(None, 2)
        if len(args) >= 3:
            markdown_note = args[2]
        else:
            return text_data, buttons
    prev = 0
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(
                    InlineKeyboardButton(text=match.group(2), url=match.group(3))
                )
            else:
                buttons.append(
                    [InlineKeyboardButton(text=match.group(2), url=match.group(3))]
                )
            text_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        else:
            text_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        text_data += markdown_note[prev:]
    return text_data, buttons


from enum import IntEnum, unique


@unique
class Types(IntEnum):
    TEXT = 1
    DOCUMENT = 2
    PHOTO = 3
    VIDEO = 4
    STICKER = 5
    AUDIO = 6
    VOICE = 7
    VIDEO_NOTE = 8
    ANIMATION = 9
    CONTACT = 11


def get_message_type(msg):
    if msg.text or msg.caption:
        return Types.TEXT
    if msg.sticker:
        return Types.STICKER
    if msg.document:
        return Types.DOCUMENT
    if msg.photo:
        return Types.PHOTO
    if msg.audio:
        return Types.AUDIO
    if msg.voice:
        return Types.VOICE
    if msg.video:
        return Types.VIDEO
    if msg.video_note:
        return Types.VIDEO_NOTE
    if msg.animation:
        return Types.ANIMATION
    if msg.contact:
        return Types.CONTACT
    return None
