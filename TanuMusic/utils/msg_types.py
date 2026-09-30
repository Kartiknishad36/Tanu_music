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
    ANIMATED_STICKER = 10
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


def get_file_id(msg):
    if msg.document:
        return msg.document.file_id
    if msg.photo:
        return msg.photo[-1].file_id if msg.photo else None
    if msg.video:
        return msg.video.file_id
    if msg.audio:
        return msg.audio.file_id
    if msg.voice:
        return msg.voice.file_id
    if msg.video_note:
        return msg.video_note.file_id
    if msg.animation:
        return msg.animation.file_id
    if msg.sticker:
        return msg.sticker.file_id
    return None
