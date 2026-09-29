import asyncio
import importlib
import sys
from pyrogram import idle
from pyrogram.errors import FloodWait

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
            try:
                await tune.boot()
            except Exception as e:
                logger.error(f"PyTgCalls boot failed: {e}")

        # Combined ONLINE (bot + assistants) — throttled in Mongo
        try:
            await app.send_online_log(userbot.clients)
        except Exception as e:
            logger.warning(f"Online log: {e}")

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
    except FloodWait as e:
        wait = int(getattr(e, "value", 60) or 60) + 10
        logger.error(
            "FloodWait %ss — sleeping in-process (do not redeploy).",
            wait,
        )
        await asyncio.sleep(wait)
        try:
            await app.boot()
            await idle()
        except Exception as e2:
            logger.error("Retry after FloodWait failed: %s", e2)
    except KeyboardInterrupt:
        logger.info("Stop signal received")
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        await asyncio.sleep(60)
        raise
    finally:
        try:
            await stop()
        except Exception:
            pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        try:
            loop.close()
        except Exception:
            pass
