from pyrogram import filters
from TanuMusic import app


@app.on_message(filters.command("dice"))
async def dice(bot, message):
    x = await bot.send_dice(message.chat.id)
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )


@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x = await bot.send_dice(message.chat.id, "🎯")
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )


@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🏀")
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )


@app.on_message(filters.command("jackpot"))
async def jackpot(bot, message):
    x = await bot.send_dice(message.chat.id, "🎰")
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )


@app.on_message(filters.command("ball"))
async def ball(bot, message):
    x = await bot.send_dice(message.chat.id, "🎳")
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )


@app.on_message(filters.command("football"))
async def football(bot, message):
    x = await bot.send_dice(message.chat.id, "⚽")
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {x.dice.value}", quote=True
    )
