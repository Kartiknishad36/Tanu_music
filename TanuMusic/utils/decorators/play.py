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
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "Bot is under maintenance. Please wait for a while."
                )
        try:
            await message.delete()
        except Exception:
            pass

        language = await get_lang(message.chat.id)
        _ = get_string(language)
        audio_telegram = (
            (
                message.reply_to_message.audio
                or message.reply_to_message.voice
            )
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (
                message.reply_to_message.video
                or message.reply_to_message.document
            )
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message) if message else None

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "play" in message.command[0]:
                    buttons = botplaylist_markup(_)
                    return await message.reply_photo(
                        photo=PLAYLIST_IMG_URL,
                        caption=_["playlist_1"],
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                return await message.reply_text(_["play_18"])

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to Fix this?",
                            callback_data="TanumousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                "You can't use this command as an Anonymous Admin.\nPlease use your real account.",
                reply_markup=upl,
            )

        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["cplay_4"])
            try:
                chat = await app.get_chat(chat_id)
            except Exception:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)

        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])

        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = False

        if message.command[0][-2] == "c":
            fplay = True
        else:
            fplay = False

        if await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text(_["call_1"])
                if get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.RESTRICTED:
                    return await message.reply_text(
                        _["call_2"].format(userbot.username, userbot.id)
                    )
            except UserNotParticipant:
                if chat_id != message.chat.id:
                    return await message.reply_text(_["call_4"])
                try:
                    try:
                        invitelink = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        return await message.reply_text(_["call_1"])
                    except Exception:
                        invitelink = await app.export_chat_invite_link(chat_id)
                    await asyncio.sleep(2)
                    await userbot.join_chat(invitelink)
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception:
                        return await message.reply_text(_["call_3"].format(userbot.name))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(_["call_3"].format(userbot.name))

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
