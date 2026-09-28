from pyrogram import filters, types, enums
from TanuMusic import app, config, lang


@app.on_message(filters.command(["admins", "admin"]) & filters.group & ~app.bl_users)
@lang.language()
async def mention_admins(_, message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass
    mentions = []
    try:
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            user = admin.user
            if user.is_bot or user.is_deleted:
                continue
            if user.username:
                mentions.append(f"@{user.username}")
            else:
                mentions.append(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>")
    except Exception:
        return await message.reply_text("Failed to fetch admins.")
    text = ", ".join(mentions) if mentions else "No admins found."
    await message.reply_text(text, disable_web_page_preview=True)
