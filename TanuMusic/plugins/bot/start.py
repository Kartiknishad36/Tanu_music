import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from TanuMusic import app
from TanuMusic.misc import _boot_
from TanuMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from TanuMusic.utils.decorators.language import LanguageStart
from TanuMusic.utils.formatters import get_readable_time
from TanuMusic.utils.inline import private_panel, start_panel
from config import BANNED_USERS, LOGGER_ID
from strings import get_string

TANU_PICS = [
    config.START_IMG_URL,
    config.YOUTUBE_IMG_URL,
    "https://telegra.ph/file/4dc854f961cd3ce46899b.jpg",
    "https://telegra.ph/file/d723f4c80da157fca1678.jpg",
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pvt(client, message: Message, _):
    try:
        await add_served_user(message.from_user.id)
    except Exception:
        pass

    bot_name = getattr(config, "MUSIC_BOT_NAME", None) or getattr(config, "BOT_NAME", "Tanu Music")
    caption = _["start_2"].format(message.from_user.mention, app.mention) if "start_2" in _ else (
        f"ʜᴇʏ {message.from_user.mention}\n\n"
        f"ɪ ᴀᴍ **{bot_name}** {app.mention}\n"
        f"ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴠᴄ ᴡɪᴛʜ /play\n\n"
        f"» ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴀᴅᴍɪɴ"
    )

    buttons = private_panel(_)
    try:
        await message.reply_photo(
            photo=random.choice([p for p in TANU_PICS if p]),
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        await message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )

    # notify log group when user starts bot in DM
    try:
        if LOGGER_ID and await is_on_off(2):
            await app.send_message(
                chat_id=LOGGER_ID,
                text=(
                    f"✦ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"✦ <b>ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n"
                    f"✦ <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username or 'N/A'}"
                ),
            )
    except Exception:
        pass


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    text = _["start_1"].format(app.mention, get_readable_time(uptime)) if "start_1" in _ else (
        f"{app.mention} ɪs ᴀʟɪᴠᴇ\n\nᴜᴘᴛɪᴍᴇ: {get_readable_time(uptime)}"
    )
    try:
        await message.reply_photo(
            photo=random.choice([p for p in TANU_PICS if p]),
            caption=text,
            reply_markup=InlineKeyboardMarkup(out),
        )
    except Exception:
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(out),
        )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text("Only for supergroups.")
                    return await app.leave_chat(message.chat.id)
                try:
                    if message.chat.id in await blacklisted_chats():
                        await message.reply_text("This chat is blacklisted.")
                        return await app.leave_chat(message.chat.id)
                except Exception:
                    pass
                await add_served_chat(message.chat.id)
                buttons = start_panel(_)
                try:
                    await message.reply_photo(
                        photo=random.choice([p for p in TANU_PICS if p]),
                        caption=(
                            f"ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ **ᴛᴀɴᴜ ᴍᴜsɪᴄ**\n\n"
                            f"ᴍᴀᴋᴇ ᴍᴇ **ᴀᴅᴍɪɴ** ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs\n"
                            f"ᴛʜᴇɴ ᴜsᴇ /play ᴛᴏ sᴛᴀʀᴛ ᴍᴜsɪᴄ"
                        ),
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
                except Exception:
                    await message.reply_text(
                        "Thanks for adding **Tanu Music**!\nUse /play after making me admin."
                    )
                # log when bot added to a group
                try:
                    if LOGGER_ID:
                        await app.send_message(
                            LOGGER_ID,
                            f"✦ ʙᴏᴛ ᴀᴅᴅᴇᴅ ᴛᴏ ɴᴇᴡ ɢʀᴏᴜᴘ\n"
                            f"✦ ᴄʜᴀᴛ: {message.chat.title}\n"
                            f"✦ ɪᴅ: <code>{message.chat.id}</code>",
                        )
                except Exception:
                    pass
        except Exception:
            pass
