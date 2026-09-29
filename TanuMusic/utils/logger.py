from pyrogram.enums import ParseMode

from TanuMusic import app
from TanuMusic.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} PLAY LOG</b>

<b>Chat ID:</b> <code>{message.chat.id}</code>
<b>Chat:</b> {message.chat.title}
<b>User:</b> {message.from_user.mention if message.from_user else 0}
<b>Query:</b> {message.text.split(None, 1)[1] if message.text and len(message.text.split())>1 else ""}
<b>Stream:</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass
"""
