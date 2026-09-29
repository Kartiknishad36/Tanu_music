from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from TanuMusic import app
from config import SUPPORT_CHANNEL, SUPPORT_CHAT


@app.on_message(filters.command(["repo", "repository"]))
async def repo(_, message: Message):
    await message.reply_text(
        "**Tanu Music** source & links:",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Updates", url=SUPPORT_CHANNEL)],
                [InlineKeyboardButton("Support", url=SUPPORT_CHAT)],
            ]
        ),
    )
