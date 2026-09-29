"""
Extra features for Tanu Music — 10 working commands.

1. /lyrics <song>     — lyrics text
2. /shuffle           — shuffle queue (keep current)
3. /clear             — clear queue (keep current or full)
4. /np | /now         — now playing card
5. /song <name>       — download audio & send as file
6. /radio [name]      — list / play radio stream
7. /id                — user + chat id
8. /reload            — reload admin cache
9. /replay            — replay current track
10. /alive            — bot status card
"""
import asyncio
import os
import random
from collections import deque

import aiohttp
from pyrogram import filters, types

from TanuMusic import app, config, db, lang, queue, tune, yt, boot
from TanuMusic.helpers import buttons, utils
from TanuMusic.helpers._dataclass import Track

# ---- Radio stations (direct stream URLs) ----
RADIO_STATIONS = {
    "lofi": {
        "title": "Lofi Hip Hop",
        "url": "https://streams.ilovemusic.de/iloveradio17.mp3",
    },
    "pop": {
        "title": "I Love Pop",
        "url": "https://streams.ilovemusic.de/iloveradio1.mp3",
    },
    "dance": {
        "title": "I Love Dance",
        "url": "https://streams.ilovemusic.de/iloveradio2.mp3",
    },
    "rock": {
        "title": "I Love Rock",
        "url": "https://streams.ilovemusic.de/iloveradio4.mp3",
    },
    "jazz": {
        "title": "I Love Chill",
        "url": "https://streams.ilovemusic.de/iloveradio10.mp3",
    },
}


def _fmt_uptime() -> str:
    import time

    sec = int(time.time() - (boot or time.time()))
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f"{h}h {m}m {s}s"


# ===================== 1. LYRICS =====================
@app.on_message(filters.command(["lyrics", "lyric"]) & ~app.bl_users)
@lang.language()
async def lyrics_cmd(_, m: types.Message):
    q = m.text.split(None, 1)[1] if len(m.command) > 1 else None
    if not q and m.reply_to_message and m.reply_to_message.text:
        q = m.reply_to_message.text
    if not q:
        return await m.reply_text("Usage: <code>/lyrics song name</code>")

    status = await m.reply_text("🔎 Searching lyrics...")
    # lyrics.ovh needs artist/title — try split or full as title
    parts = q.split("-", 1)
    if len(parts) == 2:
        artist, title = parts[0].strip(), parts[1].strip()
    else:
        artist, title = "", q.strip()

    text = None
    try:
        async with aiohttp.ClientSession() as session:
            if artist:
                url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        data = await r.json()
                        text = data.get("lyrics")
            if not text:
                # fallback: try title only as both
                url = f"https://api.lyrics.ovh/v1/{title}/{title}"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        data = await r.json()
                        text = data.get("lyrics")
    except Exception as e:
        return await status.edit_text(f"Lyrics error: <code>{e}</code>")

    if not text:
        return await status.edit_text(
            "❌ Lyrics not found.\nTry: <code>/lyrics artist - song</code>"
        )

    text = text.strip()
    if len(text) > 3500:
        text = text[:3500] + "\n\n…(truncated)"
    await status.edit_text(f"📝 <b>{q}</b>\n\n<pre>{text}</pre>")


# ===================== 2. SHUFFLE =====================
@app.on_message(filters.command(["shuffle"]) & filters.group & ~app.bl_users)
@lang.language()
async def shuffle_cmd(_, m: types.Message):
    chat_id = m.chat.id
    q = queue.queues.get(chat_id)
    if not q or len(q) < 2:
        return await m.reply_text("Queue needs at least 2 songs to shuffle.")

    current = q.popleft()
    rest = list(q)
    random.shuffle(rest)
    q.clear()
    q.append(current)
    q.extend(rest)
    await m.reply_text(f"🔀 Queue shuffled — <b>{len(rest)}</b> tracks reordered.")


# ===================== 3. CLEAR =====================
@app.on_message(
    filters.command(["clear", "clearqueue", "cqueue"]) & filters.group & ~app.bl_users
)
@lang.language()
async def clear_cmd(_, m: types.Message):
    chat_id = m.chat.id
    q = queue.queues.get(chat_id)
    if not q:
        return await m.reply_text("Queue is already empty.")

    keep = True
    if len(m.command) > 1 and m.command[1].lower() in ("all", "full"):
        keep = False

    if keep and len(q) >= 1:
        current = q[0]
        n = len(q) - 1
        q.clear()
        q.append(current)
        await m.reply_text(f"🗑 Cleared <b>{n}</b> queued tracks (current kept).")
    else:
        n = len(q)
        queue.clear(chat_id)
        await m.reply_text(f"🗑 Cleared full queue (<b>{n}</b> tracks).")


# ===================== 4. NOW PLAYING =====================
@app.on_message(
    filters.command(["np", "now", "current"]) & filters.group & ~app.bl_users
)
@lang.language()
async def np_cmd(_, m: types.Message):
    chat_id = m.chat.id
    if not await db.get_call(chat_id):
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))

    media = queue.get_current(chat_id)
    if not media:
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))

    playing = await db.playing(chat_id)
    status = "▶ Playing" if playing else "⏸ Paused"
    title = getattr(media, "title", "Unknown")
    dur = getattr(media, "duration", "?")
    user = getattr(media, "user", "—")
    url = getattr(media, "url", "")
    thumb_url = getattr(media, "thumbnail", None) or config.DEFAULT_THUMB

    text = (
        f"{status}\n"
        f"🎵 <b>{title}</b>\n"
        f"⏱ {dur}\n"
        f"👤 {user}\n"
    )
    if url:
        text += f"🔗 <a href='{url}'>Open</a>"

    try:
        if thumb_url:
            await m.reply_photo(
                photo=thumb_url,
                caption=text,
                reply_markup=buttons.controls(chat_id, is_playing=playing),
            )
        else:
            await m.reply_text(
                text, reply_markup=buttons.controls(chat_id, is_playing=playing)
            )
    except Exception:
        await m.reply_text(
            text, reply_markup=buttons.controls(chat_id, is_playing=playing)
        )


# ===================== 5. SONG DOWNLOAD =====================
@app.on_message(filters.command(["song", "mp3"]) & ~app.bl_users)
@lang.language()
async def song_cmd(_, m: types.Message):
    q = m.text.split(None, 1)[1] if len(m.command) > 1 else None
    if not q:
        return await m.reply_text("Usage: <code>/song song name</code>")

    status = await m.reply_text("⬇️ Searching & downloading...")
    try:
        track = await yt.search(q, m.id, music=True)
        if not track:
            return await status.edit_text("❌ No results found.")

        path = await yt.download(
            track.id, is_live=getattr(track, "is_live", False), video=False
        )
        if not path or not os.path.exists(path):
            return await status.edit_text("❌ Download failed.")

        await status.edit_text("📤 Uploading...")
        await m.reply_audio(
            audio=path,
            title=track.title[:64],
            performer=getattr(track, "channel_name", "YouTube")[:64],
            duration=int(getattr(track, "duration_sec", 0) or 0),
            caption=f"🎵 <b>{track.title}</b>\n🔗 {track.url}",
        )
        await status.delete()
        try:
            os.remove(path)
        except Exception:
            pass
    except Exception as e:
        await status.edit_text(f"Error: <code>{e}</code>")


# ===================== 6. RADIO =====================
@app.on_message(filters.command(["radio"]) & filters.group & ~app.bl_users)
@lang.language()
async def radio_cmd(_, m: types.Message):
    if not tune or not getattr(tune, "clients", None):
        return await m.reply_text("VC engine not ready.")

    arg = m.command[1].lower() if len(m.command) > 1 else None
    if not arg:
        lines = ["📻 <b>Radio stations</b>\n"]
        for key, st in RADIO_STATIONS.items():
            lines.append(f"• <code>/radio {key}</code> — {st['title']}")
        return await m.reply_text("\n".join(lines))

    st = RADIO_STATIONS.get(arg)
    if not st:
        return await m.reply_text(
            f"Unknown station. Use <code>/radio</code> for list."
        )

    chat_id = m.chat.id
    status = await m.reply_text(f"📻 Starting <b>{st['title']}</b>...")

    track = Track(
        id=f"radio_{arg}",
        channel_name="Radio",
        duration="LIVE",
        duration_sec=0,
        title=st["title"],
        url=st["url"],
        file_path=st["url"],
        is_live=True,
        user=m.from_user.mention if m.from_user else "—",
        message_id=m.id,
    )

    try:
        queue.clear(chat_id)
        queue.put(chat_id, track)
        await db.add_call(chat_id)
        await tune.play_media(chat_id, status, track)
        await status.edit_text(
            f"📻 Now playing radio: <b>{st['title']}</b>",
            reply_markup=buttons.controls(chat_id),
        )
    except Exception as e:
        await status.edit_text(f"Radio failed: <code>{e}</code>")


# ===================== 7. ID =====================
@app.on_message(filters.command(["id"]) & ~app.bl_users)
@lang.language()
async def id_cmd(_, m: types.Message):
    user = m.from_user
    if m.reply_to_message and m.reply_to_message.from_user:
        user = m.reply_to_message.from_user

    chat = m.chat
    lines = [
        f"👤 <b>User</b>",
        f"• Name: {user.mention if user else '—'}",
        f"• ID: <code>{user.id if user else '—'}</code>",
        f"• Username: @{user.username if user and user.username else 'None'}",
        f"",
        f"💬 <b>Chat</b>",
        f"• Title: {chat.title or 'Private'}",
        f"• ID: <code>{chat.id}</code>",
        f"• Type: {chat.type}",
    ]
    await m.reply_text("\n".join(lines))


# ===================== 8. RELOAD ADMINS =====================
@app.on_message(filters.command(["reload"]) & filters.group & ~app.bl_users)
@lang.language()
async def reload_cmd(_, m: types.Message):
    try:
        admins = await db.get_admins(m.chat.id, reload=True)
        await m.reply_text(
            m.lang.get("admin_cache_reloaded", "✅ Admin cache reloaded.")
            + f"\nAdmins: <b>{len(admins)}</b>"
        )
    except Exception as e:
        await m.reply_text(f"Reload failed: <code>{e}</code>")


# ===================== 9. REPLAY =====================
@app.on_message(filters.command(["replay"]) & filters.group & ~app.bl_users)
@lang.language()
async def replay_cmd(_, m: types.Message):
    chat_id = m.chat.id
    if not await db.get_call(chat_id):
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))

    media = queue.get_current(chat_id)
    if not media:
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))

    status = await m.reply_text("↻ Replaying...")
    try:
        await tune.replay(chat_id)
        await status.edit_text(
            f"↻ Replaying: <b>{getattr(media, 'title', 'track')}</b>",
            reply_markup=buttons.controls(chat_id),
        )
    except Exception as e:
        await status.edit_text(f"Replay failed: <code>{e}</code>")


# ===================== 10. ALIVE =====================
@app.on_message(filters.command(["alive", "status"]) & ~app.bl_users)
@lang.language()
async def alive_cmd(_, m: types.Message):
    from TanuMusic import userbot as ub

    assistants = len(getattr(ub, "clients", []) or [])
    active = len(getattr(db, "active_calls", {}) or {})
    text = (
        f"💚 <b>Tanu Music is alive</b>\n\n"
        f"• Bot: @{app.username}\n"
        f"• Assistants: <code>{assistants}</code>\n"
        f"• Active VC: <code>{active}</code>\n"
        f"• Uptime: <code>{_fmt_uptime()}</code>\n"
        f"• Version: <code>3.0.1</code>"
    )
    try:
        await m.reply_photo(
            photo=config.PING_IMG or config.START_IMG,
            caption=text,
            reply_markup=buttons.ping_markup("Support"),
        )
    except Exception:
        await m.reply_text(text, reply_markup=buttons.ping_markup("Support"))
