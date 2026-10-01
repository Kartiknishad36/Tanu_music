import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from TanuMusic import Carbon, YouTube, app
from TanuMusic.core.call import BABY
from TanuMusic.misc import db
from TanuMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    is_active_chat,
    is_video_allowed,
)
from TanuMusic.utils.exceptions import AssistantErr
from TanuMusic.utils.inline.play import stream_markup, telegram_markup
from TanuMusic.utils.stream.queue import put_queue, put_queue_index
from TanuMusic.utils.thumbnails import gen_thumb


async def stream(
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if video:
        if not await is_video_allowed(chat_id):
            raise AssistantErr("Video play is not allowed in this chat.")
    if forceplay:
        await BABY.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = f"**Queued Playlist**\n\n"
        count = 0
        for search in result:
            if int(count) == getattr(config, "PLAYLIST_FETCH_LIMIT", 25):
                break
            try:
                title, duration_min, duration_sec, thumbnail, vidid = search
                if str(duration_min) == "None":
                    continue
                if duration_sec > config.DURATION_LIMIT:
                    continue
                file_path = await YouTube.download(
                    vidid, mystic, video=bool(video), videoid=True
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if file_path else vidid,
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                count += 1
                msg += f"{count}. {title[:40]}\n"
            except Exception:
                continue
        await mystic.edit_text(msg or "Playlist queued.")
        return

    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        file_path = await YouTube.download(vidid, mystic, videoid=True, video=status)
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if file_path else vidid,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                f"**Added to queue** at position **#{position}**\n\n**Title:** {title}\n**Duration:** {duration_min}\n**Requested by:** {user_name}"
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await BABY.join_call(
                chat_id,
                original_chat_id,
                file_path if file_path else vidid,
                video=status,
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if file_path else vidid,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, chat_id) if False else stream_markup(
                {}, chat_id
            )
            try:
                from strings import get_string
                from TanuMusic.utils.database import get_lang

                language = await get_lang(original_chat_id)
                _ = get_string(language)
                button = stream_markup(_, chat_id)
            except Exception:
                button = stream_markup({}, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img if img else config.YOUTUBE_IMG_URL,
                caption=f"**Now Playing**\n\n**Title:** [{title}]({link})\n**Duration:** {duration_min}\n**Requested by:** {user_name}",
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()

    elif streamtype == "soundcloud":
        file_path = result["path"]
        title = result["title"]
        duration_min = result.get("duration_min", "00:00")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                result.get("id", file_path),
                user_id,
                "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                f"**Added to queue** #{position}\n**Title:** {title}"
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await BABY.join_call(chat_id, original_chat_id, file_path, video=None)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                result.get("id", file_path),
                user_id,
                "audio",
                forceplay=forceplay,
            )
            await mystic.edit_text(f"**Now Playing**\n**Title:** {title}")

    elif streamtype == "telegram":
        file_path = result["path"]
        link = result.get("link", "")
        title = result.get("title", "Telegram Media")
        duration_min = result.get("dur", "00:00")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                file_path,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(f"**Added to queue** #{position}\n**Title:** {title}")
        else:
            if not forceplay:
                db[chat_id] = []
            await BABY.join_call(
                chat_id, original_chat_id, file_path, video=bool(video)
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                file_path,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = telegram_markup({}, chat_id)
            try:
                from strings import get_string
                from TanuMusic.utils.database import get_lang

                language = await get_lang(original_chat_id)
                _ = get_string(language)
                button = telegram_markup(_, chat_id)
            except Exception:
                pass
            run = await app.send_photo(
                original_chat_id,
                photo=config.TELEGRAM_AUDIO_URL,
                caption=f"**Now Playing**\n**Title:** {title}\n**Requested by:** {user_name}",
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            try:
                await mystic.delete()
            except Exception:
                pass

    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = "Live"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(f"**Live added to queue** #{position}")
        else:
            if not forceplay:
                db[chat_id] = []
            await BABY.join_call(
                chat_id, original_chat_id, link, video=status, live=True
            )
            await put_queue(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            await mystic.edit_text(f"**Live streaming started**\n**Title:** {title}")

    else:
        # index / direct link
        file_path = result
        title = "Index Stream"
        duration_min = "00:00"
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                file_path,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(f"**Added to queue** #{position}")
        else:
            if not forceplay:
                db[chat_id] = []
            await BABY.join_call(
                chat_id, original_chat_id, file_path, video=bool(video)
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                file_path,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            await mystic.edit_text(f"**Now Playing (Index)**")
