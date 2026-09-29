import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.misc import SUDOERS
from TanuMusic.utils.database import get_served_chats, get_served_users


@app.on_message(filters.command(["broadcast", "gcast"]) & SUDOERS)
async def broadcast(_, message: Message):
    if not message.reply_to_message and len(message.command) < 2:
        return await message.reply_text("Reply to a message or /broadcast text")
    text = None if message.reply_to_message else message.text.split(None, 1)[1]
    chats = await get_served_chats()
    users = await get_served_users()
    targets = list(set(chats + users))
    status = await message.reply_text(f"Broadcasting to {len(targets)} targets...")
    sent = failed = 0
    for chat_id in targets:
        try:
            if message.reply_to_message:
                await message.reply_to_message.copy(chat_id)
            else:
                await app.send_message(chat_id, text)
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy(chat_id)
                else:
                    await app.send_message(chat_id, text)
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    await status.edit_text(f"Broadcast done. Sent: {sent} | Failed: {failed}")
