import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from TanuMusic import app
from TanuMusic.core.call import BABY
from TanuMusic.misc import db
from TanuMusic.utils.database import (
    get_lang,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from config import BANNED_USERS, adminlist
from strings import get_string


def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        return user_id in adminlist.get(chat_id, [])
    except Exception:
        return False


@app.on_callback_query(filters.regex(r"^ADMIN") & ~BANNED_USERS)
async def admin_callback_handler(_, CallbackQuery: CallbackQuery):
    try:
        callback_data = CallbackQuery.data.strip()
        # e.g. ADMIN Resume|-100123 or ADMIN Pause|0
        parts = callback_data.split(None, 1)
        if len(parts) < 2:
            return await CallbackQuery.answer("Invalid", show_alert=True)
        command = parts[1]
        if "|" not in command:
            return await CallbackQuery.answer("Invalid", show_alert=True)

        action, chat_id_str = command.split("|", 1)
        chat_id = int(chat_id_str.split("_")[0])
        if chat_id == 0:
            chat_id = CallbackQuery.message.chat.id

        user_id = CallbackQuery.from_user.id

        # permission: chat admin / auth / nonadmin mode
        try:
            if not await is_nonadmin_chat(chat_id):
                if not is_admin(chat_id, user_id):
                    member = await app.get_chat_member(chat_id, user_id)
                    if member.status not in ("creator", "administrator"):
                        return await CallbackQuery.answer(
                            "Only admins can control the player.", show_alert=True
                        )
        except Exception:
            pass

        language = await get_lang(chat_id)
        _ = get_string(language)

        if not await is_active_chat(chat_id):
            return await CallbackQuery.answer(
                _.get("admin_6", "No active stream."), show_alert=True
            )

        action = action.strip()

        if action == "Pause":
            if not await is_music_playing(chat_id):
                return await CallbackQuery.answer(
                    _.get("admin_1", "Already paused."), show_alert=True
                )
            await music_off(chat_id)
            await BABY.pause_stream(chat_id)
            await CallbackQuery.answer("Paused ⏸")
            try:
                await CallbackQuery.message.reply_text(
                    _.get("admin_2", "Stream paused.").format(
                        CallbackQuery.from_user.mention
                    )
                )
            except Exception:
                pass

        elif action == "Resume":
            if await is_music_playing(chat_id):
                return await CallbackQuery.answer(
                    _.get("admin_3", "Already playing."), show_alert=True
                )
            await music_on(chat_id)
            await BABY.resume_stream(chat_id)
            await CallbackQuery.answer("Resumed ▶")
            try:
                await CallbackQuery.message.reply_text(
                    _.get("admin_4", "Stream resumed.").format(
                        CallbackQuery.from_user.mention
                    )
                )
            except Exception:
                pass

        elif action == "Stop" or action == "End":
            await BABY.stop_stream(chat_id)
            await CallbackQuery.answer("Stopped ⏹")
            try:
                await CallbackQuery.message.reply_text(
                    _.get("admin_5", "Stream ended.").format(
                        CallbackQuery.from_user.mention
                    )
                )
            except Exception:
                pass

        elif action == "Skip":
            check = db.get(chat_id)
            if not check or len(check) < 2:
                await BABY.stop_stream(chat_id)
                await CallbackQuery.answer("Queue empty — stopped")
                return
            # pop current and play next via change_stream path
            try:
                popped = check.pop(0)
            except Exception:
                popped = None
            if not check:
                await BABY.stop_stream(chat_id)
                await CallbackQuery.answer("Queue empty — stopped")
                return
            await CallbackQuery.answer("Skipped ⏭")
            try:
                # force next track
                from TanuMusic.utils.stream.autoclear import auto_clean

                if popped:
                    await auto_clean(popped)
            except Exception:
                pass
            # re-join stream for next item
            try:
                queued = check[0]
                file_path = queued.get("file")
                video = str(queued.get("streamtype", "")) == "video"
                await BABY.skip_stream(chat_id, file_path, video=video)
            except Exception as e:
                await BABY.stop_stream(chat_id)
                await CallbackQuery.answer(f"Skip error: {e}", show_alert=True)

        elif action == "Loop":
            await set_loop(chat_id, 3)
            await CallbackQuery.answer("Loop x3 enabled")

        elif action == "Shuffle":
            check = db.get(chat_id)
            if check and len(check) > 2:
                first = check[0]
                rest = check[1:]
                import random

                random.shuffle(rest)
                db[chat_id] = [first] + rest
                await CallbackQuery.answer("Queue shuffled")
            else:
                await CallbackQuery.answer("Not enough tracks", show_alert=True)

        else:
            await CallbackQuery.answer(f"{action}", show_alert=False)

    except Exception as e:
        try:
            await CallbackQuery.answer(str(e)[:200], show_alert=True)
        except Exception:
            pass
