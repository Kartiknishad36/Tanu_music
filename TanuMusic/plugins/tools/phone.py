import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command(["phone", "number"]))
async def phone_info(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /phone +9198xxxxxxxx")
    number = message.command[1]
    try:
        parsed = phonenumbers.parse(number, None)
        text = (
            f"**Number:** {number}\n"
            f"**Valid:** {phonenumbers.is_valid_number(parsed)}\n"
            f"**Region:** {geocoder.description_for_number(parsed, 'en')}\n"
            f"**Carrier:** {carrier.name_for_number(parsed, 'en')}\n"
            f"**Timezone:** {timezone.time_zones_for_number(parsed)}\n"
        )
        await message.reply_text(text)
    except Exception as e:
        await message.reply_text(f"Error: {e}")
