from pyrogram import filters, types
from TanuMusic import app, db, lang
from TanuMusic.helpers import utils


@app.on_message(filters.command(["blacklist", "unblacklist"]) & app.sudo_filter)
@lang.language()
async def _bl(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang.get("user_not_found", "User not found"))
    if m.command[0].startswith("un"):
        await db.del_blacklist(user.id)
        app.bl_users = app.bl_users.filter  # keep filter object
        await m.reply_text(m.lang.get("bl_removed", "Removed {}").format(user.mention))
    else:
        await db.add_blacklist(user.id)
        await m.reply_text(m.lang.get("bl_added", "Blacklisted {}").format(user.mention))
