import time
from asyncio import sleep

from pyrogram import enums, filters
from TanuMusic import app


@app.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status not in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent = await message.reply_text("Only admins can use this.")
        await sleep(5)
        return await sent.delete()
    sent_message = await message.reply_text("Getting information...")
    deleted_acc = premium_acc = banned = bot = uncached = 0
    async for ban in app.get_chat_members(
        message.chat.id, filter=enums.ChatMembersFilter.BANNED
    ):
        banned += 1
    async for member in app.get_chat_members(message.chat.id):
        u = member.user
        if u.is_deleted:
            deleted_acc += 1
        elif u.is_bot:
            bot += 1
        elif u.is_premium:
            premium_acc += 1
        else:
            uncached += 1
    timelog = "{:.2f}".format(time.perf_counter() - start_time)
    await sent_message.edit(
        f"**{message.chat.title}**\nMembers: {count}\nBots: {bot}\nZombies: {deleted_acc}\nBanned: {banned}\nPremium: {premium_acc}\nTime: {timelog}s"
    )
