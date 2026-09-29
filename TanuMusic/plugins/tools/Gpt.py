from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["gpt", "ask"]))
async def gpt_cmd(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /gpt your question")
    q = " ".join(message.command[1:])
    await message.reply_text(
        f"Question: {q}\n\nGPT API not configured. Set your AI key in config to enable."
    )
