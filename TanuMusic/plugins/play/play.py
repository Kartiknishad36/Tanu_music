import random
import string

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TanuMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from TanuMusic.core.call import Call
from TanuMusic.utils.database import is_video_allowed
from TanuMusic.utils.decorators.play import PlayWrapper
from TanuMusic.utils.formatters import formats
from TanuMusic.utils.inline.play import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from TanuMusic.utils.logger import play_logs
from TanuMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical


@app.on_message(
    filters.command(["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"])
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    mystic = await message.reply_text(
        _["play_1"].format(message.from_user.first_name) if _ else "Processing..."
    )
    try:
        await mystic.edit("🔍 Searching...")
    except:
        pass

    if url:
        query = message.text.split(None, 1)[1]
    else:
        if len(message.command) < 2:
            if message.reply_to_message:
                if message.reply_to_message.audio or message.reply_to_message.voice:
                    try:
                        details = {
                            "path": await message.reply_to_message.download(),
                            "link": message.reply_to_message.link or "",
                            "title": getattr(message.reply_to_message.audio, "title", None)
                            or getattr(message.reply_to_message.voice, "file_unique_id", "Telegram Audio"),
                            "dur": "00:00",
                        }
                        await stream(
                            mystic,
                            message.from_user.id,
                            details,
                            chat_id,
                            message.from_user.first_name,
                            message.chat.id,
                            video=video,
                            streamtype="telegram",
                            forceplay=fplay,
                        )
                        return await play_logs(message, streamtype="Telegram")
                    except Exception as e:
                        return await mystic.edit_text(f"Play error: {e}")
                elif message.reply_to_message.video or message.reply_to_message.document:
                    try:
                        details = {
                            "path": await message.reply_to_message.download(),
                            "link": message.reply_to_message.link or "",
                            "title": "Telegram Video",
                            "dur": "00:00",
                        }
                        await stream(
                            mystic,
                            message.from_user.id,
                            details,
                            chat_id,
                            message.from_user.first_name,
                            message.chat.id,
                            video=True,
                            streamtype="telegram",
                            forceplay=fplay,
                        )
                        return await play_logs(message, streamtype="Telegram")
                    except Exception as e:
                        return await mystic.edit_text(f"Play error: {e}")
            return await mystic.edit_text(
                _["play_2"] if _ else "Reply to audio/video or give a song name / YouTube link."
            )
        query = message.text.split(None, 1)[1]

    # Index / direct URL stream
    if query.startswith(("http://", "https://")) and not any(
        x in query for x in ["youtube", "youtu.be", "spotify", "soundcloud", "apple", "resso"]
    ):
        try:
            await stream(
                mystic,
                message.from_user.id,
                query,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=video,
                streamtype="index",
                forceplay=fplay,
            )
            return await play_logs(message, streamtype="Index")
        except Exception as e:
            return await mystic.edit_text(f"Play error: {e}")

    # Spotify
    if "spotify.com" in query:
        try:
            details, track_id = await Spotify.track(query)
            await stream(
                mystic,
                message.from_user.id,
                details,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=video,
                streamtype="youtube",
                forceplay=fplay,
            )
            return await play_logs(message, streamtype="Spotify")
        except Exception as e:
            return await mystic.edit_text(f"Spotify error: {e}")

    # SoundCloud
    if "soundcloud.com" in query:
        try:
            details, track_path = await SoundCloud.track(query)
            await stream(
                mystic,
                message.from_user.id,
                {"path": track_path, "title": details.get("title", "SoundCloud"), "dur": details.get("duration_min", "00:00"), "link": query},
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=False,
                streamtype="telegram",
                forceplay=fplay,
            )
            return await play_logs(message, streamtype="SoundCloud")
        except Exception as e:
            return await mystic.edit_text(f"SoundCloud error: {e}")

    # YouTube / search
    try:
        if "youtube.com" in query or "youtu.be" in query:
            results = await YouTube.track(query)
        else:
            results = await YouTube.search(query)
        if not results:
            return await mystic.edit_text("No results found.")

        # Single track
        if isinstance(results, dict) or (isinstance(results, list) and len(results) == 1):
            track = results[0] if isinstance(results, list) else results
            details = {
                "title": track.get("title") or track[0] if isinstance(track, (list, tuple)) else str(track),
                "link": track.get("link") or query,
                "vidid": track.get("id") or track.get("vidid") or "",
                "duration_min": track.get("duration_min") or track.get("duration") or "00:00",
            }
            if isinstance(track, (list, tuple)) and len(track) >= 5:
                details = {
                    "title": track[0],
                    "duration_min": track[1],
                    "duration_sec": track[2],
                    "link": track[3] if len(track) > 3 else query,
                    "vidid": track[4] if len(track) > 4 else "",
                }
            await stream(
                mystic,
                message.from_user.id,
                details,
                chat_id,
                message.from_user.first_name,
                message.chat.id,
                video=video,
                streamtype="youtube",
                forceplay=fplay,
            )
            return await play_logs(message, streamtype="YouTube")

        # Multiple results -> show slider or take first
        track = results[0]
        if isinstance(track, (list, tuple)):
            details = {
                "title": track[0],
                "duration_min": track[1] if len(track) > 1 else "00:00",
                "vidid": track[4] if len(track) > 4 else "",
                "link": f"https://www.youtube.com/watch?v={track[4]}" if len(track) > 4 else query,
            }
        else:
            details = track
        await stream(
            mystic,
            message.from_user.id,
            details,
            chat_id,
            message.from_user.first_name,
            message.chat.id,
            video=video,
            streamtype="youtube",
            forceplay=fplay,
        )
        return await play_logs(message, streamtype="YouTube")
    except NoActiveGroupCall:
        return await mystic.edit_text(
            "No active voice chat. Start a VC first or make sure the assistant can join."
        )
    except Exception as e:
        return await mystic.edit_text(f"Play error: {e}")
