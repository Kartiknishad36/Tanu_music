import asyncio
import importlib
import sys
from pyrogram import idle

if sys.platform != "win32":
    try:
        import resource

        _soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        _target = min(65536, _hard)
        if _soft < _target:
            resource.setrlimit(resource.RLIMIT_NOFILE, (_target, _hard))
    except Exception:
        pass

from TanuMusic import tune, app, config, db, logger, stop, userbot, yt
from TanuMusic.plugins import all_modules


async def main():
    try:
        await db.connect()

        await app.boot()
        await userbot.boot()

        if not userbot.clients:
            logger.error(
                "No assistant started. Set STRING_SESSION in env. Music will not play."
            )
        else:
            await tune.boot()

        loaded = 0
        for module in all_modules:
            try:
                importlib.import_module(f"TanuMusic.plugins.{module}")
                loaded += 1
            except Exception as e:
                logger.error(f"Failed to load plugin {module}: {e}", exc_info=True)
        logger.info(f"Loaded {loaded}/{len(all_modules)} plugin modules.")

        if config.COOKIES_URL:
            try:
                await yt.save_cookies(config.COOKIES_URL)
            except Exception as e:
                logger.error(f"Failed to download cookies: {e}")

        try:
            sudoers = await db.get_sudoers()
            app.sudoers.update(sudoers)
            try:
                app.sudo_filter.update(list(app.sudoers))
            except Exception:
                app.sudo_filter = __import__("pyrogram").filters.user(list(app.sudoers))
        except Exception as e:
            logger.warning(f"Sudo load warning: {e}")

        try:
            bl = await db.get_blacklisted()
            try:
                app.bl_users.update(bl)
            except Exception:
                app.bl_users = __import__("pyrogram").filters.user(bl or [0])
        except Exception as e:
            logger.warning(f"Blacklist load warning: {e}")

        logger.info(f"Loaded {len(app.sudoers)} sudo users.")
        logger.info("Bot started successfully! Ready to play music.")

        try:
            await idle()
        except KeyboardInterrupt:
            logger.info("Stop signal received...")
    finally:
        await stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
