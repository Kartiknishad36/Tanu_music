from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import db
from TanuMusic.utils.decorators import language
from config import BANNED_USERS


@app.on_message(filters.command(["queue", "cqueue"]) & filters.group & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    chat_id = message.chat.id
    if chat_id not in db or not db[chat_id]:
        return await message.reply_text(_["queue_2"])
    text = _["queue_1"] if "queue_1" in _ else "**Queue:**\n"
    for i, track in enumerate(db[chat_id][:15], 1):
        text += f"{i}. {track.get('title', 'Unknown')} - {track.get('by', '')}\n"
    await message.reply_text(text)
