import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from TanuMusic import LOGGER, app, userbot
from TanuMusic.core.call import BABY
from TanuMusic.misc import sudo
from TanuMusic.plugins import ALL_MODULES
from TanuMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill A Pyrogram Session")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("TanuMusic.plugins" + all_module)
    LOGGER("TanuMusic.plugins").info("All Features Loaded — Tanu Music")
    await userbot.start()
    await BABY.start()
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TanuMusic").warning(
            "Log group VC not active — bot continues (start VC in LOGGER group for full features)."
        )
    except Exception:
        pass
    await BABY.decorators()
    LOGGER("TanuMusic").info("Tanu Music started successfully")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("TanuMusic").info("Tanu Music stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
