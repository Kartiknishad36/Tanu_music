from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter, ParseMode
from TanuMusic import app, lang

@app.on_message(filters.command("bots") & filters.group)
@lang.language()
async def list_bots(client, message: Message):
    try:
        await message.delete()
    except Exception:
        pass

    try:
        bot_list = []
        bot_count = 0
        status_msg = await message.reply_text(message.lang["bots_scanning"], parse_mode=ParseMode.HTML)

        async for member in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.BOTS):
            bot_count += 1
            bot_username = f"@{member.user.username}" if member.user.username else "No Username"
            bot_list.append(
                f"{bot_count}. <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> - {bot_username}"
            )

        if bot_count == 0:
            await status_msg.edit_text(message.lang["bots_none"], parse_mode=ParseMode.HTML)
            return

        response = message.lang["bots_title"].format(message.chat.title)
        response += "<blockquote>" + "\n".join(bot_list) + "</blockquote>"
        response += message.lang["bots_total"].format(bot_count)

        await status_msg.edit_text(response, disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    except Exception as e:
        if "FLOOD_WAIT" not in str(e):
            try:
                await message.reply_text(message.lang["bots_error"].format(str(e)), parse_mode=ParseMode.HTML)
            except Exception:
                pass
