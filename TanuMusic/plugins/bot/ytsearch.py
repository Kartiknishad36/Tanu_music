import logging

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

from TanuMusic import app
from config import BANNED_USERS


@app.on_message(filters.command(["search", "ytsearch"]) & ~BANNED_USERS)
async def ytsearch(_, message: Message):
    try:
        await message.delete()
    except Exception:
        pass
    try:
        if len(message.command) < 2:
            return await message.reply_text("**Usage:**\n/search [query]")
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 Searching...")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"Title - {results[i]['title']}\n"
            text += f"Duration - {results[i]['duration']}\n"
            text += f"Views - {results[i]['views']}\n"
            text += f"Channel - {results[i]['channel']}\n"
            text += f"https://youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))
