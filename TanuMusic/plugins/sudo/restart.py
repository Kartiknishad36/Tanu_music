import os
import shutil
from pyrogram import filters
from TanuMusic import app
from TanuMusic.misc import SUDOERS


@app.on_message(filters.command(["restart", "reboot"]) & SUDOERS)
async def restart_bot(_, message):
    m = await message.reply_text("Restarting Tanu Music...")
    try:
        shutil.rmtree("downloads", ignore_errors=True)
        shutil.rmtree("cache", ignore_errors=True)
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("cache", exist_ok=True)
    except Exception:
        pass
    await m.edit_text("Restarting... please wait 10-20s")
    os.system(f"kill -9 {os.getpid()} && bash start")
