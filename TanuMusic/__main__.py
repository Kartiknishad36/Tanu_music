import asyncio
import importlib
import sys
from pyrogram import idle

if sys.platform != "win32":
    try:
        import resource

        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        target = min(65536, hard)
        if soft < target:
            resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
    except Exception:
        pass

from TanuMusic import (
    app,
    config,
    db,
    logger,
    stop,
    tune,
    userbot,
    yt,
)
from TanuMusic.plugins import all_modules


async def main():
    try:
        await db.connect()

        await app.boot()
        await userbot.boot()

        if not userbot.clients:
            logger.error(
                "No assistant started. Check STRING_SESSION in Railway variables."
            )
        else:
            await tune.boot()

        loaded = 0
        for module in all_modules:
            try:
                importlib.import_module(f"TanuMusic.plugins.{module}")
                loaded += 1
            except Exception as e:
                logger.error(f"Failed to load plugin {module}: {e}")
        logger.info(f"Loaded {loaded}/{len(all_modules)} plugins")

        if getattr(config, "COOKIES_URL", None):
            try:
                await yt.save_cookies(config.COOKIES_URL)
            except Exception as e:
                logger.error(f"Cookies download failed: {e}")

        try:
            sudoers = await db.get_sudoers()
            app.sudoers.update(sudoers or [])
            try:
                app.sudo_filter.update(list(app.sudoers))
            except Exception:
                import pyrogram

                app.sudo_filter = pyrogram.filters.user(list(app.sudoers))
        except Exception as e:
            logger.warning(f"Sudo load: {e}")

        try:
            bl = await db.get_blacklisted()
            try:
                app.bl_users.update(bl or [])
            except Exception:
                import pyrogram

                app.bl_users = pyrogram.filters.user(bl or [0])
        except Exception as e:
            logger.warning(f"Blacklist load: {e}")

        logger.info(f"Sudo users: {len(app.sudoers)}")
        logger.info("Tanu Music started successfully — ready!")

        await idle()
    except KeyboardInterrupt:
        logger.info("Stop signal received")
    finally:
        await stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
