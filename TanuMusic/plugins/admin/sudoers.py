from pyrogram import filters, types

from TanuMusic import app, db, lang
from TanuMusic.helpers import utils


@app.on_message(filters.command(["addsudo", "delsudo", "rmsudo"]) & app.sudo_filter)
@lang.language()
async def _sudo(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang["user_not_found"])

    if m.command[0] == "addsudo":
        if user.id in app.sudoers:
            return await m.reply_text(m.lang["sudo_already"].format(user.mention))

        app.sudoers.add(user.id)
        app.sudo_filter.update([user.id])
        await db.add_sudo(user.id)
        await m.reply_text(m.lang["sudo_added"].format(user.mention))
    else:
        if user.id not in app.sudoers:
            return await m.reply_text(m.lang["sudo_not"].format(user.mention))

        app.sudoers.discard(user.id)
        app.sudo_filter.update([])
        app.sudo_filter.update(app.sudoers)
        await db.del_sudo(user.id)
        await m.reply_text(m.lang["sudo_removed"].format(user.mention))


@app.on_message(filters.command(["listsudo", "sudolist"]) & app.sudo_filter)
@lang.language()
async def _listsudo(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    sent = await m.reply_text(m.lang["sudo_fetching"])

    owner_user = await app.get_users(app.owner)
    o_mention = f"{owner_user.mention} ({app.owner})"

    txt = m.lang["sudo_owner"].format(o_mention)
    sudoers = await db.get_sudoers()

    if sudoers:
        sudo_list = ""
        for user_id in sudoers:
            try:
                user = await app.get_users(user_id)
                sudo_list += f"\n- {user.mention} ({user_id})"
            except Exception:
                sudo_list += f"\n- Deleted Account ({user_id})"
        txt += m.lang["sudo_list"].format(sudo_list)
    else:
        txt += m.lang.get("sudo_empty", "\nNo additional sudo users.")

    await sent.edit_text(txt)
