import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.errors import FloodWait

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

    # Bot start with FloodWait handling
    while True:
        try:
            await app.start()
            break
        except FloodWait as e:
            wait = int(e.value) if hasattr(e, "value") else int(getattr(e, "x", 60))
            LOGGER(__name__).warning(f"FloodWait {wait}s — sleeping (do not restart)...")
            await asyncio.sleep(wait + 5)
        except Exception as e:
            LOGGER(__name__).error(f"Bot start failed: {e}")
            raise

    # Load plugins one-by-one (skip broken ones)
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("TanuMusic.plugins" + all_module)
        except Exception as e:
            LOGGER("TanuMusic.plugins").error(
                f"Skipped plugin {all_module}: {type(e).__name__}: {e}"
            )
    LOGGER("TanuMusic.plugins").info("Plugins loaded — Tanu Music")

    try:
        await userbot.start()
    except Exception as e:
        LOGGER(__name__).warning(f"Userbot start issue: {e}")

    try:
        await BABY.start()
    except Exception as e:
        LOGGER(__name__).warning(f"PyTgCalls start issue: {e}")

    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("TanuMusic").warning(
            "Log group VC not active — bot continues."
        )
    except Exception:
        pass

    try:
        await BABY.decorators()
    except Exception as e:
        LOGGER(__name__).warning(f"decorators: {e}")

    LOGGER("TanuMusic").info("Tanu Music started successfully")
    await idle()
    await app.stop()
    try:
        await userbot.stop()
    except Exception:
        pass
    LOGGER("TanuMusic").info("Tanu Music stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
