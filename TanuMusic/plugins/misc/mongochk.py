from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app
from TanuMusic.misc import SUDOERS
from config import MONGO_DB_URI


@app.on_message(filters.command(["mongochk", "mongo"]) & SUDOERS)
async def mongo_chk(_, message: Message):
    if not MONGO_DB_URI:
        return await message.reply_text("MONGO_DB_URI not set.")
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        client = AsyncIOMotorClient(MONGO_DB_URI, serverSelectionTimeoutMS=5000)
        await client.server_info()
        await message.reply_text("MongoDB connection OK ✅")
    except Exception as e:
        await message.reply_text(f"MongoDB error: {e}")
