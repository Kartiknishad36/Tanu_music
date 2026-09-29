from telegraph import upload_file
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["tgm", "telegraph"]))
async def telegraph_ul(_, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.reply_text("Reply to a media file.")
    i = await message.reply("Making link...")
    try:
        path = await reply.download()
        fk = upload_file(path)
        url = "https://telegra.ph" + fk[0]
        await i.edit(f"Your link: {url}")
    except Exception as e:
        await i.edit(f"Error: {e}")


@app.on_message(filters.command(["graph", "grf"]))
async def graph_ul(_, message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.reply_text("Reply to a media file.")
    i = await message.reply("Making link...")
    try:
        path = await reply.download()
        fk = upload_file(path)
        url = "https://graph.org" + fk[0]
        await i.edit(f"Your link: {url}")
    except Exception as e:
        await i.edit(f"Error: {e}")
