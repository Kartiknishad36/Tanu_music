import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import PLAYLIST_IMG_URL, adminlist
from strings import get_string
from TanuMusic import YouTube, app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_served_private_chat,
)
from TanuMusic.utils.inline import botplaylist_markup


def PlayWrapper(command):
    async def wrapper(client, message):
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception:
            _ = get_string("en")

        try:
            if await is_maintenance() is False:
                if message.from_user and message.from_user.id not in SUDOERS:
                    return await message.reply_text(
                        "Bot is under maintenance. Please wait."
                    )
        except Exception:
            pass

        try:
            if await is_commanddelete_on(message.chat.id):
                await message.delete()
        except Exception:
            pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )

        try:
            url = await YouTube.url(message)
        except Exception:
            url = None

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "play" in message.command[0].lower():
                    buttons = botplaylist_markup(_)
                    try:
                        return await message.reply_photo(
                            photo=PLAYLIST_IMG_URL,
                            caption=_.get("playlist_1", "Usage: /play [song name or youtube link]"),
                            reply_markup=InlineKeyboardMarkup(buttons),
                        )
                    except Exception:
                        return await message.reply_text(
                            _.get("playlist_1", "Usage: /play [song name or youtube link]")
                        )
                return await message.reply_text(
                    _.get("play_18", "Usage: /play [song name or youtube link]")
                )

        if message.sender_chat:
            return await message.reply_text(
                "Anonymous admin detected. Please use your user account."
            )

        video = (
            True
            if message.command[0][0] in ["v", "c"] and message.command[0][1] not in ["c", "p"]
            or message.command[0][0:2] in ["cv"]
            else False
        )
        if message.command[0][0] == "c" or message.command[0][0:2] == "cv":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(
                    _.get("cplay_1", "Channel play mode is disabled. Enable with /channelplay")
                )
            try:
                chat = await app.get_chat(chat_id)
            except Exception:
                return await message.reply_text("Failed to get linked channel.")
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        try:
            playmode = await get_playmode(message.chat.id)
        except Exception:
            playmode = "Direct"
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(
                        "Admin list not updated. Use /reload"
                    )
                if message.from_user.id not in admins:
                    return await message.reply_text(
                        _.get("play_4", "Only admins can play.")
                    )

        if message.command[0][0] == "c" or message.command[0][0:2] == "cv":
            try:
                await app.get_chat_member(chat_id, app.id)
            except Exception:
                return await message.reply_text(
                    "Bot is not present in the linked channel."
                )

        # Ensure assistant joins the group for VC
        try:
            userbot = await get_assistant(chat_id)
            if userbot is None:
                return await message.reply_text(
                    "No assistant available. Check STRING_SESSION."
                )
            try:
                await userbot.get_chat_member(chat_id, userbot.id)
            except UserNotParticipant:
                try:
                    invite_link = await app.export_chat_invite_link(chat_id)
                except ChatAdminRequired:
                    return await message.reply_text(
                        "Give bot invite users permission, then try again."
                    )
                except Exception as e:
                    return await message.reply_text(f"Invite link error: {e}")
                try:
                    await userbot.join_chat(invite_link)
                except InviteRequestSent:
                    return await message.reply_text(
                        "Assistant join request sent. Approve it and retry /play."
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(f"Assistant join failed: {e}")
        except Exception as e:
            return await message.reply_text(f"Assistant error: {type(e).__name__}: {e}")

        fplay = True if "force" in message.command[0].lower() else None
        return await command(
            client, message, _, chat_id, video, channel, playmode, url, fplay
        )

    return wrapper
