from pyrogram import filters, types
from TanuMusic import app, tune, db, lang


@app.on_callback_query(filters.regex(r"^(pause|resume|skip|stop)_(-?\d+)$"))
@lang.language()
async def control_cb(_, q: types.CallbackQuery):
    action, chat_id = q.data.split("_")
    chat_id = int(chat_id)
    if action == "pause":
        await tune.pause(chat_id)
        await q.answer("Paused")
    elif action == "resume":
        await tune.resume(chat_id)
        await q.answer("Resumed")
    elif action == "skip":
        await tune.play_next(chat_id)
        await q.answer("Skipped")
    elif action == "stop":
        await tune.stop(chat_id)
        await q.answer("Stopped")


@app.on_callback_query(filters.regex(r"^noop$"))
async def noop(_, q: types.CallbackQuery):
    await q.answer()
