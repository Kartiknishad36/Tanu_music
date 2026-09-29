import requests
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["git", "github"]))
async def gitinfo(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /git username")
    user = message.command[1]
    try:
        r = requests.get(f"https://api.github.com/users/{user}", timeout=10).json()
        text = (
            f"**Name:** {r.get('name')}\n"
            f"**Username:** {r.get('login')}\n"
            f"**Bio:** {r.get('bio')}\n"
            f"**Repos:** {r.get('public_repos')}\n"
            f"**Followers:** {r.get('followers')}\n"
            f"**URL:** {r.get('html_url')}\n"
        )
        if r.get("avatar_url"):
            await message.reply_photo(r["avatar_url"], caption=text)
        else:
            await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
