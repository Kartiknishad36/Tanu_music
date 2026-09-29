from faker import Faker
from pyrogram import filters
from TanuMusic import app

fake = Faker()


@app.on_message(filters.command(["fake", "fakeinfo"]))
async def fake_info(_, message):
    text = (
        f"**Name:** {fake.name()}\n"
        f"**Address:** {fake.address()}\n"
        f"**Email:** {fake.email()}\n"
        f"**Phone:** {fake.phone_number()}\n"
        f"**Job:** {fake.job()}\n"
    )
    await message.reply_text(text)
