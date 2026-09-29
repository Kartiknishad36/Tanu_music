from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

from TanuMusic import app
from config import SUPPORT_CHAT

MUST_JOIN = SUPPORT_CHAT  # set SUPPORT_CHAT in config / env


@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            # if MUST_JOIN is invite link, skip membership check
            if "t.me/+" in str(MUST_JOIN) or "joinchat" in str(MUST_JOIN):
                return
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            link = MUST_JOIN if str(MUST_JOIN).startswith("http") else f"https://t.me/{MUST_JOIN}"
            try:
                await msg.reply_text(
                    f"Please join support first then use the bot.\n{link}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Join", url=link)]]
                    ),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        pass
    except Exception:
        pass
