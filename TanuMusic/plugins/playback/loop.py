from pyrogram import filters, types

from TanuMusic import app, db, lang
from TanuMusic.helpers import can_manage_vc


@app.on_message(filters.command(["loop"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _loop(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    current_loop = await db.get_loop(m.chat.id)

    if len(m.command) > 1:
        mode_arg = m.command[1].lower()
        if mode_arg in ["0", "disable"]:
            new_loop = 0
            text = m.lang["loop_disabled"]
        elif mode_arg in ["single", "1", "one"]:
            new_loop = 1
            text = m.lang["loop_single"]
        elif mode_arg in ["queue", "all", "10"]:
            new_loop = 10
            text = m.lang["loop_queue_set"]
        else:
            return await m.reply_text(m.lang["loop_usage"])
    else:
        if current_loop == 0:
            new_loop = 1
            text = m.lang["loop_single"]
        elif current_loop == 1:
            new_loop = 10
            text = m.lang["loop_queue_set"]
        else:
            new_loop = 0
            text = m.lang["loop_disabled"]

    await db.set_loop(m.chat.id, new_loop)
    await m.reply_text(text)
