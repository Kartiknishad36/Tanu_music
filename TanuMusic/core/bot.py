import asyncio
from typing import Optional

import pyrogram
from pyrogram.errors import FloodWait

from TanuMusic import config, logger


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
        # Telegram FloodWait on auth.ImportBotAuthorization — wait, don't crash-loop
        attempts = 0
        while True:
            attempts += 1
            try:
                await super().start()
                break
            except FloodWait as e:
                wait = int(getattr(e, "value", 0) or 0) + 5
                logger.error(
                    "FloodWait on bot login: wait %s seconds (~%s min). "
                    "Do NOT redeploy — Railway restart makes it worse.",
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

        try:
            if self.logger:
                await self.send_message(
                    self.logger,
                    f"🤖 <b>Tanu Music</b> started\n<code>{self.id}</code> @{self.username}",
                )
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
                "Log group fail (LOGGER_ID=%s): %s — add bot as admin & fix ID.",
                self.logger,
                ex,
            )

        logger.info(f"🤖 Bot started successfully as @{self.username}")

    async def exit(self) -> None:
        try:
            await super().stop()
        except Exception:
            pass
        logger.info("🤖 Bot client stopped.")
