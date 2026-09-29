import asyncio
import os
import time
from typing import Optional

import pyrogram
from pyrogram.errors import FloodWait

from TanuMusic import config, logger

# Restart spam prevent — same process / rapid redeploys
_START_FLAG = "/tmp/tanumusic_log_sent"
_THROTTLE_SEC = 600  # 10 minutes


def _should_send_log() -> bool:
    try:
        if os.path.exists(_START_FLAG):
            age = time.time() - os.path.getmtime(_START_FLAG)
            if age < _THROTTLE_SEC:
                return False
        with open(_START_FLAG, "w") as f:
            f.write(str(time.time()))
        return True
    except Exception:
        return True


class Bot(pyrogram.Client):

    def __init__(self):
        super().__init__(
            name="TanuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
            in_memory=True,
        )

        self.owner: int = config.OWNER_ID
        self.logger: int = config.LOGGER_ID
        self.bl_users: pyrogram.filters.Filter = pyrogram.filters.user()
        self.sudoers: set = {self.owner}
        self.sudo_filter: pyrogram.filters.Filter = pyrogram.filters.user(self.owner)

        self.id: Optional[int] = None
        self.name: Optional[str] = None
        self.username: Optional[str] = None
        self.mention: Optional[str] = None

    async def boot(self) -> None:
        attempts = 0
        while True:
            attempts += 1
            try:
                await super().start()
                break
            except FloodWait as e:
                wait = int(getattr(e, "value", 0) or 0) + 5
                logger.error(
                    "FloodWait on bot login: wait %s sec (~%s min). Do NOT redeploy.",
                    wait,
                    max(1, wait // 60),
                )
                if attempts > 3:
                    raise
                await asyncio.sleep(wait)
            except Exception as e:
                logger.error("Bot start failed: %s", e)
                raise

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        # ONE start log only (anti spam on Railway restarts)
        if self.logger and _should_send_log():
            try:
                text = (
                    f"🤖 <b>Tanu Music ONLINE</b>\n"
                    f"• Bot: @{self.username}\n"
                    f"• ID: <code>{self.id}</code>\n"
                    f"• Version: 3.0.1"
                )
                await self.send_message(self.logger, text)
                try:
                    member = await self.get_chat_member(self.logger, self.id)
                    if member.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
                        logger.warning(
                            "Bot is not admin in LOGGER group %s — promote bot.",
                            self.logger,
                        )
                except Exception:
                    pass
            except Exception as ex:
                logger.error(
                    "Log group fail (LOGGER_ID=%s): %s",
                    self.logger,
                    ex,
                )
        else:
            logger.info("Skipped duplicate start log (throttle 10 min)")

        logger.info(f"🤖 Bot started successfully as @{self.username}")

    async def exit(self) -> None:
        try:
            await super().stop()
        except Exception:
            pass
        logger.info("🤖 Bot client stopped.")
