from pyrogram import filters, types
from TanuMusic import app, config


@app.on_message(filters.new_chat_members & filters.group)
async def new_chat_member(_, message: types.Message):
    for member in message.new_chat_members:
        if member.id == app.id:
            chat = message.chat
            chat_name = chat.title
            chat_id = chat.id
            chat_username = f"@{chat.username}" if chat.username else "Private group"
            try:
                members_count = await app.get_chat_members_count(chat_id)
            except Exception:
                members_count = "?"

            added_by = message.from_user
            added_by_name = added_by.mention if added_by else "Unknown"

            text = f"""<blockquote>🟢 <b>Tanu Music added in a new group</b></blockquote>

<blockquote>
🔖 <b>Chat name:</b> {chat_name}
🆔 <b>Chat ID:</b> <code>{chat_id}</code>
👤 <b>Username:</b> {chat_username}
👥 <b>Members:</b> {members_count}
🤵 <b>Added by:</b> {added_by_name}
</blockquote>
"""
            try:
                await app.send_photo(
                    chat_id=config.LOGGER_ID,
                    photo=config.START_IMG,
                    caption=text,
                )
            except Exception as e:
                print(f"Failed to send new chat notification: {e}")
            break


@app.on_message(filters.left_chat_member & filters.group)
async def left_chat_member(_, message: types.Message):
    if message.left_chat_member and message.left_chat_member.id == app.id:
        chat = message.chat
        chat_name = chat.title
        chat_id = chat.id
        chat_username = f"@{chat.username}" if chat.username else "Private group"
        removed_by = message.from_user
        removed_by_name = removed_by.mention if removed_by else "Unknown"

        text = f"""<blockquote>🔴 <b>Tanu Music removed from a group</b></blockquote>

<blockquote>
🔖 <b>Chat name:</b> {chat_name}
🆔 <b>Chat ID:</b> <code>{chat_id}</code>
👤 <b>Username:</b> {chat_username}
🚫 <b>Removed by:</b> {removed_by_name}
</blockquote>
"""
        try:
            await app.send_photo(
                chat_id=config.LOGGER_ID,
                photo=config.START_IMG,
                caption=text,
            )
        except Exception as e:
            print(f"Failed to send left chat notification: {e}")
