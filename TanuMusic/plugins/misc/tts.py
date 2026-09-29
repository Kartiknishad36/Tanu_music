from pyrogram import filters
from gtts import gTTS
from TanuMusic import app


@app.on_message(filters.command("tts"))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /tts your text")
    text = message.text.split(" ", 1)[1]
    tts = gTTS(text=text, lang="hi")
    tts.save("speech.mp3")
    await client.send_audio(message.chat.id, "speech.mp3")
