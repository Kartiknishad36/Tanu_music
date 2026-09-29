import os
from random import randint
from typing import Union

from pyrogram.types import InlineKeyboardMarkup

import config
from TanuMusic import Carbon, YouTube, app
from TanuMusic.core.call import Call
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
        await Call.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = f"**Queued Playlist**\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_LIMIT:
                break
            try:
                title, duration_min, duration_sec, thumbnail, vidid = search
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:30]}\n"
                msg += f"   └ Position: {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(
                        vidid, mystic, video=status, videoid=True
                    )
                except Exception:
                    return await mystic.edit_text("Failed to download from YouTube.")
                await Call.join_call(
                    chat_id, original_chat_id, file_path, video=status
                )
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                img = await gen_thumb(vidid, user_id)
                button = stream_markup({}, vidid)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=f"**Streaming**\n\n**Title:** [{title[:27]}](https://t.me/{app.username}?start=info_{vidid})\n**Duration:** {duration_min}\n**By:** {user_name}",
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        else:
            await mystic.edit_text(msg)
            return
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(
                vidid, mystic, videoid=True, video=status
            )
        except Exception:
            return await mystic.edit_text("Failed to process YouTube track.")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                f"**Added to Queue**\n\n**Title:** {title[:27]}\n**Position:** {position}"
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Call.join_call(
                chat_id, original_chat_id, file_path, video=status
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid, user_id)
            button = stream_markup({}, vidid)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=f"**Streaming**\n\n**Title:** [{title[:27]}](https://t.me/{app.username}?start=info_{vidid})\n**Duration:** {duration_min}\n**By:** {user_name}",
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()
    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        duration_min = result.get("dur", "00:00")
        title = result.get("title", "Telegram Media")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                "telegram",
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                f"**Added to Queue**\n\n**Title:** {title[:27]}\n**Position:** {position}"
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await Call.join_call(
                chat_id, original_chat_id, file_path, video=video
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                "telegram",
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = telegram_markup({})
            run = await app.send_photo(
                original_chat_id,
                photo=config.TELEGRAM_AUDIO_URL if not video else config.TELEGRAM_VIDEO_URL,
                caption=f"**Streaming from Telegram**\n\n**Title:** {title[:27]}\n**Duration:** {duration_min}\n**By:** {user_name}",
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
    elif streamtype == "index":
        link = result
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_" + link,
                "Index Link",
                "Unknown",
                user_name,
                "index",
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(f"**Index link added to queue at position {position}**")
        else:
            if not forceplay:
                db[chat_id] = []
            await Call.join_call(
                chat_id, original_chat_id, link, video=video
            )
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_" + link,
                "Index Link",
                "Unknown",
                user_name,
                "index",
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = telegram_markup({})
            run = await app.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=f"**Streaming Index**\n\n**By:** {user_name}",
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
