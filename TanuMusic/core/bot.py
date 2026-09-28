# ===============================================================================
# bot.py - Main Bot Client Manager
# ===============================================================================
import pyrogram
from typing import Optional

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
            link_preview_options=pyrogram.types.LinkPreviewOptions(
                is_disabled=True),
        )

        self.owner: int = config.OWNER_ID
        self.logger: int = config.LOGGER_ID
        self.bl_users: pyrogram.filters.Filter = pyrogram.filters.user()
        self.sudoers: set = {self.owner}
        self.sudo_filter: pyrogram.filters.Filter = pyrogram.filters.user(
            self.owner)

        self.id: Optional[int] = None
        self.name: Optional[str] = None
        self.username: Optional[str] = None
        self.mention: Optional[str] = None

    async def boot(self) -> None:
        await super().start()

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
                member = await self.get_chat_member(self.logger, self.id)
                if member.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
                    logger.warning(
                        "Bot is not admin in LOGGER group %s — promote bot.",
                        self.logger,
                    )
        except Exception as ex:
            logger.error(
                "Log group fail (LOGGER_ID=%s): %s — add bot as admin & fix ID.",
                self.logger,
                ex,
            )

        logger.info(f"🤖 Bot started successfully as @{self.username}")

    async def exit(self) -> None:
        await super().stop()
        logger.info("🤖 Bot client stopped.")
