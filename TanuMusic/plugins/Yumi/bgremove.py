import os
import aiohttp
import aiofiles
from aiohttp import ContentTypeError
from TanuMusic import app as app
from pyrogram import filters

async def remove_bg(filepath):
    headers = {"X-API-Key": "a4BNNo5HDmg95p67umhfQJk4"}
    form = aiohttp.FormData()
    form.add_field("image_file", open(filepath, "rb"))
    form.add_field("size", "auto")
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post("https://api.remove.bg/v1.0/removebg", data=form) as r:
            if r.status == 200:
                content = await r.read()
                out = filepath.replace(".jpg", "_nobg.png").replace(".png", "_nobg.png")
                async with aiofiles.open(out, "wb") as f:
                    await f.write(content)
                return out
            else:
                return None

@app.on_message(filters.command(["rmbg", "removebg", "bgremove"]))
async def rmbg(client, message):
    reply = message.reply_to_message
    if not reply or not reply.photo:
        return await message.reply("Reply to a photo")
    msg = await message.reply("Removing background...")
    try:
        photo = await reply.download()
        result = await remove_bg(photo)
        if result:
            await message.reply_document(result)
            await msg.delete()
            os.remove(photo)
            os.remove(result)
        else:
            await msg.edit("Failed to remove background")
    except Exception as e:
        await msg.edit(f"Error: {e}")
