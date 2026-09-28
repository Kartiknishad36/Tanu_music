import asyncio
from pyrogram import filters, types
from pyrogram.errors import FloodWait, RPCError
from TanuMusic import app, db, lang


@app.on_message(filters.command(["broadcast"]) & app.sudo_filter)
@lang.language()
async def broadcast_cmd(_, m: types.Message):
    if not m.reply_to_message and len(m.command) < 2:
        return await m.reply_text("Usage: /broadcast <text> or reply with /broadcast")
    chats = await db.get_chats()
    if not chats:
        return await m.reply_text("No chats tracked yet.")
    status = await m.reply_text(f"Broadcasting to {len(chats)} chats...")
    sent = failed = 0
    for chat_id in chats:
        try:
            if m.reply_to_message:
                await m.reply_to_message.copy(chat_id)
            else:
                text = m.text.split(None, 1)[1]
                await app.send_message(chat_id, text)
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except RPCError:
            failed += 1
    await status.edit_text(f"Done. Sent: {sent}, failed: {failed}")
