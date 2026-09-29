import whois
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("domain"))
async def get_domain_info(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /domain example.com")
    domain_name = message.command[1]
    try:
        domain_info = whois.whois(domain_name)
        response = (
            f"**Domain:** {domain_info.domain_name}\n"
            f"**Registrar:** {domain_info.registrar}\n"
            f"**Created:** {domain_info.creation_date}\n"
            f"**Expires:** {domain_info.expiration_date}"
        )
        await message.reply_text(response)
    except Exception as e:
        await message.reply_text(f"Failed: {e}")
