import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from TanuMusic import userbot as us, app
from TanuMusic.core.userbot import assistants


@app.on_message(filters.command("sg"))
async def sg(client: Client, message: Message):
    if len(message.text.split()) < 1 and not message.reply_to_message:
        return await message.reply("sg username/id/reply")
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = message.text.split()[1]
        except:
            return await message.reply("sg username/id/reply")
    try:
        user = await client.get_users(user_id)
    except Exception:
        return await message.reply("User not found")
    lol = await message.reply("🔍 Searching history...")
    try:
        for i in assistants:
            try:
                await us[i].send_message("@Sangmata_bot", f"{user.id}")
                await asyncio.sleep(2)
            except Exception:
                continue
        await asyncio.sleep(3)
        async for msg in us[1].get_chat_history("@Sangmata_bot", limit=5):
            if msg.text and str(user.id) in msg.text:
                await lol.edit(msg.text)
                try:
                    await us[1].invoke(DeleteHistory(peer=await us[1].resolve_peer("@Sangmata_bot"), max_id=0, revoke=True))
                except:
                    pass
                return
        await lol.edit("No history found or SangMata unavailable.")
    except Exception as e:
        await lol.edit(f"Error: {e}")
