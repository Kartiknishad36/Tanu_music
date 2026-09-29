from pyrogram import enums, filters, types

from TanuMusic import app, config, db, lang
from TanuMusic.helpers import buttons, utils


@app.on_message(filters.command(["help"]) & filters.private & ~app.bl_users)
@lang.language()
async def _help(_, m: types.Message):
    try:
        await m.delete()
    except Exception:
        pass

    caption = m.lang.get(
        "help_menu",
        "<b>Click the buttons below for command info.</b>\nAll commands work with /",
    )
    try:
        await m.reply_photo(
            photo=config.START_IMG,
            caption=caption,
            reply_markup=buttons.help_markup(m.lang),
        )
    except Exception:
        await m.reply_text(text=caption, reply_markup=buttons.help_markup(m.lang))


@app.on_callback_query(filters.regex(r"^help"))
@lang.language()
async def help_cb(_, q: types.CallbackQuery):
    data = q.data or ""
    texts = {
        "help": q.message.lang.get(
            "help_menu",
            "<b>Help — Tanu Music</b>\nUse the buttons below.",
        )
        if hasattr(q.message, "lang")
        else "<b>Help — Tanu Music</b>",
        "help_play": (
            "<b>🎵 Play</b>\n"
            "/play song name — play audio\n"
            "/vplay song — play video\n"
            "/skip /pause /resume /stop\n"
            "/queue /loop"
        ),
        "help_admin": (
            "<b>🛡 Admin</b>\n"
            "/playmode — only admins can play\n"
            "/auth /unauth — authorize users\n"
            "/settings"
        ),
        "help_tools": (
            "<b>🔧 Tools</b>\n"
            "/ping /stats /activevc\n"
            "/lang — language"
        ),
        "help_sudo": (
            "<b>👑 Sudo</b>\n"
            "/broadcast /restart /logs\n"
            "/addsudo /delsudo"
        ),
    }
    text = texts.get(data, texts.get("help", "Help"))
    try:
        await q.message.edit_caption(
            caption=text,
            reply_markup=buttons.help_markup(
                getattr(q.message, "lang", {}) or {}
            ),
        )
    except Exception:
        try:
            await q.message.edit_text(
                text,
                reply_markup=buttons.help_markup(
                    getattr(q.message, "lang", {}) or {}
                ),
            )
        except Exception:
            pass
    await q.answer()


@app.on_message(filters.command(["start"]))
@lang.language()
async def start(_, message: types.Message):
    if message.chat.type != enums.ChatType.PRIVATE:
        try:
            await message.delete()
        except Exception:
            pass

    if not message.from_user:
        return

    # Blacklist check via db list (not Filter object)
    try:
        bl = getattr(db, "blacklisted", []) or []
        if message.from_user.id in bl:
            return await message.reply_text(
                message.lang.get("bl_user_notify", "You are blacklisted.")
            )
    except Exception:
        pass

    if len(message.command) > 1 and message.command[1] == "help":
        return await _help(_, message)

    private = message.chat.type == enums.ChatType.PRIVATE
    name = message.from_user.first_name or "User"
    bot_name = app.name or config.BOT_NAME or "Tanu Music"

    _text = (
        message.lang.get("start_pm", "Hey {0}, this is <b>{1}</b>!\nYour music player is ready.").format(
            name, bot_name
        )
        if private
        else message.lang.get("start_gp", "Hey, this is <b>{0}</b>\nA music player bot.").format(
            bot_name
        )
    )

    key = buttons.start_key(message.lang, private)
    photo = config.START_IMG or config.DEFAULT_THUMB
    try:
        await message.reply_photo(photo=photo, caption=_text, reply_markup=key)
    except Exception:
        await message.reply_text(text=_text, reply_markup=key)

    if private:
        try:
            if await db.is_user(message.from_user.id):
                return
            await utils.send_log(message)
            await db.add_user(message.from_user.id)
        except Exception:
            pass


@app.on_message(filters.command(["playmode", "settings"]) & filters.group & ~app.bl_users)
@lang.language()
async def settings(_, message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass

    admin_only = await db.get_play_mode(message.chat.id)
    await utils.safe_text(
        message,
        message.lang.get("start_settings", "Settings for <b>{}</b>").format(
            message.chat.title or "chat"
        ),
        reply_markup=buttons.settings_markup(
            message.lang, admin_only, "en", message.chat.id
        ),
        quote=True,
    )


@app.on_message(filters.new_chat_members, group=7)
@lang.language()
async def _new_member(_, message: types.Message):
    if message.chat.type != enums.ChatType.SUPERGROUP:
        try:
            return await message.chat.leave()
        except Exception:
            return

    for member in message.new_chat_members:
        if member.id == app.id:
            if await db.is_chat(message.chat.id):
                return
            await db.add_chat(message.chat.id)
