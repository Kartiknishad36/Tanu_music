import asyncio
import logging
from pyrogram import filters, types
from pyrogram.errors import FloodWait, ChatSendPlainForbidden, ChatWriteForbidden

from TanuMusic import tune, app, db, lang, queue, yt, userbot
from TanuMusic.helpers import buttons, utils
from TanuMusic.helpers._play import checkUB

logger = logging.getLogger(__name__)


async def safe_reply(message, text, **kwargs):
    try:
        return await message.reply_text(text, **kwargs)
    except (ChatSendPlainForbidden, ChatWriteForbidden):
        return None
    except Exception as e:
        logger.error(f"safe_reply: {e}")
        return None


@app.on_message(
    filters.command(["play", "playforce", "vplay", "vplayforce"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
@checkUB
async def play_hndlr(_, m: types.Message) -> None:
    try:
        await m.delete()
    except Exception:
        pass

    chat_id = m.chat.id
    force = "force" in m.command[0].lower()
    video = m.command[0].lower().startswith("vplay")

    if not userbot.clients:
        return await safe_reply(
            m,
            "❌ No assistant connected.\n"
            "Owner: set <code>STRING_SESSION</code> in Railway Variables.",
        )

    if video:
        if not await db.get_vplay_enabled():
            return await safe_reply(m, "Video play is disabled.")

    query = m.text.split(None, 1)[1] if len(m.command) > 1 else None
    if not query and not (m.reply_to_message and m.reply_to_message.media):
        return await safe_reply(m, m.lang.get("play_usage", "Usage: /play <song name>"))

    sent = await safe_reply(m, m.lang.get("play_processing", "🔎 Searching..."))
    if not sent:
        return

    try:
        track = await yt.search(query, m.id, music=not video) if query else None

        if not track:
            await sent.edit_text(
                m.lang.get(
                    "play_no_results",
                    "❌ No results found.\nTry another name or paste a YouTube link.",
                )
            )
            return

        track.user = m.from_user.mention if m.from_user else "User"
        track.video = video

        await sent.edit_text(f"⬇️ Downloading: <b>{track.title}</b>")
        path = await yt.download(
            track.id, is_live=getattr(track, "is_live", False), video=video
        )
        if not path:
            await sent.edit_text(
                "❌ Download failed.\n"
                "• Refresh YouTube cookies (COOKIE_URL)\n"
                "• Or try another song / direct YT link"
            )
            return

        track.file_path = path

        if force:
            queue.force_add(chat_id, track)
        else:
            queue.put(chat_id, track)

        if not await db.get_call(chat_id):
            await db.add_call(chat_id)
            await tune.play_media(chat_id, sent, track)
            try:
                await sent.edit_text(
                    m.lang.get("play_now", "▶️ Now playing: <b>{}</b>").format(
                        track.title
                    ),
                    reply_markup=buttons.controls(chat_id),
                )
            except Exception:
                pass
            try:
                await utils.play_log(m, track.title, track.duration)
            except Exception:
                pass
        else:
            pos = max(0, len(queue.get_queue(chat_id)) - 1)
            try:
                await sent.edit_text(
                    m.lang.get("play_queued", "➕ Queued at #{} — <b>{}</b>").format(
                        pos, track.title
                    ),
                )
            except Exception:
                pass
    except Exception as e:
        logger.exception("play error")
        err = str(e).strip() or type(e).__name__
        try:
            await sent.edit_text(f"❌ Play error: <code>{err[:400]}</code>")
        except Exception:
            pass
