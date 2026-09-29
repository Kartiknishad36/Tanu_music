import requests
from bs4 import BeautifulSoup as BSP
from pyrogram import filters
from TanuMusic import app

url = "https://all-hashtag.com/library/contents/ajax_generator.php"


@app.on_message(filters.command("hastag"))
async def hastag(bot, message):
    try:
        text = message.text.split(" ", 1)[1]
        data = dict(keyword=text, filter="top")
        res = requests.post(url, data).text
        content = BSP(res, "html.parser").find("div", {"class": "copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n/hastag python")
    except Exception as e:
        return await message.reply_text(f"Error: {e}")
    await message.reply_text(f"Hashtags:\n<pre>{content}</pre>", quote=True)
