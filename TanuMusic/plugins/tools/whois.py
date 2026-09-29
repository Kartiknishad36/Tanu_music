from pyrogram import filters
from pyrogram.types import Message
from TanuMusic import app


@app.on_message(filters.command(["whois", "info"]))
async def whois_cmd(_, message: Message):
    try:
        if message.reply_to_message and message.reply_to_message.from_user:
            user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            user = await app.get_users(message.command[1])
        else:
            user = message.from_user
        text = (
            f"**Name:** {user.first_name} {user.last_name or ''}\n"
            f"**ID:** `{user.id}`\n"
            f"**Username:** @{user.username if user.username else 'None'}\n"
            f"**Bot:** {user.is_bot}\n"
            f"**Premium:** {getattr(user, 'is_premium', False)}\n"
        )
        if user.photo:
            await message.reply_photo(user.photo.big_file_id, caption=text)
        else:
            await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
