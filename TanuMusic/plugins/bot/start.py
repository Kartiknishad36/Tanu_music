import time
import random

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from TanuMusic import app
from TanuMusic.misc import _boot_
from TanuMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from TanuMusic.utils.decorators.language import LanguageStart
from TanuMusic.utils.formatters import get_readable_time
from TanuMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

TANU_PICS = [
    "https://graph.org/file/f76fd86d1936d45a63c64.jpg",
    "https://graph.org/file/69ba894371860cd22d92e.jpg",
    "https://graph.org/file/67fde88d8c3aa8327d363.jpg",
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pvt(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.reply_photo(
        photo=random.choice(TANU_PICS),
        caption=_["start_2"].format(config.MUSIC_BOT_NAME, app.mention)
        if "start_2" in _
        else f"Welcome to **Tanu Music** {message.from_user.mention}!\n\nPlay music in your group VC with /play",
        reply_markup=private_panel(_),
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_text(
        _["start_1"].format(app.mention, get_readable_time(uptime))
        if "start_1" in _
        else f"{app.mention} is alive | uptime: {get_readable_time(uptime)}",
        reply_markup=InlineKeyboardMarkup(out[0] if isinstance(out, tuple) else out),
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
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text("This chat is blacklisted.")
                    return await app.leave_chat(message.chat.id)
                await add_served_chat(message.chat.id)
                await message.reply_photo(
                    photo=random.choice(TANU_PICS),
                    caption=f"Thanks for adding **Tanu Music**!\n\nUse /play to start music.",
                )
        except Exception:
            pass
