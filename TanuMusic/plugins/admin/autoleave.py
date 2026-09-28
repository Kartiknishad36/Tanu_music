from pyrogram import filters
from pyrogram.types import Message

from TanuMusic import app, db


@app.on_message(
    filters.command(["autoleave"])
    & filters.group
    & ~app.bl_users
)
async def autoleave_command(_, m: Message) -> None:
    if m.from_user.id not in app.sudoers:
        return await m.reply_text("❌ Only sudo users can use this command.")

    if len(m.command) < 2:
        current_status = await db.get_autoleave(m.chat.id)
        status_text = "enabled" if current_status else "disabled"
        return await m.reply_text(
            f"<blockquote>🔧 Auto leave status: {status_text}</blockquote>\n\n"
            "<blockquote><b>Usage:</b>\n"
            "• `/autoleave enable`\n"
            "• `/autoleave disable`</blockquote>"
        )

    subcommand = m.command[1].lower()

    if subcommand == "enable":
        await db.set_autoleave(m.chat.id, True)
        await m.reply_text("✅ Auto leave enabled (leave VC after 5 min idle).")
    elif subcommand == "disable":
        await db.set_autoleave(m.chat.id, False)
        await m.reply_text("✅ Auto leave disabled.")
    else:
        await m.reply_text("❌ Use `/autoleave enable` or `/autoleave disable`")
