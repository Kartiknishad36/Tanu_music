from io import BytesIO

import aiohttp
from pyrogram import filters

from TanuMusic import app


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@app.on_message(filters.command("carbon"))
async def _carbon(client, message):
    replied = message.reply_to_message
    if not replied or not (replied.text or replied.caption):
        return await message.reply_text("Reply to a text message to make carbon.")
    text = await message.reply("Processing...")
    carbon = await make_carbon(replied.text or replied.caption)
    await text.edit("Uploading...")
    await message.reply_photo(carbon)
    await text.delete()
    carbon.close()
