from pyrogram import filters
from TanuMusic import app
from config import OWNER_ID

@app.on_message(filters.command("raid") & filters.user(OWNER_ID))
async def raid_cmd(client, message):
    await message.reply("Raid command is disabled for safety. Use only in private controlled environments.")
