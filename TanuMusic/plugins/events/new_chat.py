from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app
from TanuMusic.utils.database import add_served_chat


@app.on_message(filters.new_chat_members & filters.group)
async def new_chat_member(_, message: Message):
    try:
        for member in message.new_chat_members:
            if member.id == app.id:
                try:
                    await add_served_chat(message.chat.id)
                except Exception:
                    pass
                try:
                    await message.reply_text(
                        f"Thanks for adding **Tanu Music**.\n"
                        f"Use /play to start music."
                    )
                except Exception:
                    pass
    except Exception:
        pass
