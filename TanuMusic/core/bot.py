import asyncio
import time
from typing import Optional

import pyrogram
from pyrogram.errors import FloodWait

from TanuMusic import config, logger

# Cross-restart throttle via Mongo (Railway /tmp is wiped every deploy)
_THROTTLE_SEC = 600  # 10 minutes


async def _should_send_log() -> bool:
    try:
        from TanuMusic import db

        doc = await db.cache.find_one({"_id": "start_log"})
        now = time.time()
        if doc:
            last = float(doc.get("ts", 0) or 0)
            if now - last < _THROTTLE_SEC:
                return False
        await db.cache.update_one(
            {"_id": "start_log"},
            {"$set": {"ts": now}},
            upsert=True,
        )
        return True
    except Exception:
        return True


async def _sleep_flood(wait: int, label: str = "bot") -> None:
    """Sleep full FloodWait with heartbeat so Railway sees activity."""
    wait = max(int(wait), 5)
    logger.error(
        "⏳ FloodWait %s: sleeping %s sec (~%s min). DO NOT REDEPLOY — wait will reset.",
        label,
        wait,
        max(1, wait // 60),
    )
    remaining = wait
    chunk = 60  # log every minute
    while remaining > 0:
        step = min(chunk, remaining)
        await asyncio.sleep(step)
        remaining -= step
        if remaining > 0:
            logger.info(
                "⏳ FloodWait %s: %s sec left (~%s min)...",
                label,
                remaining,
                max(1, remaining // 60),
            )
    logger.info("✅ FloodWait %s done — retrying login...", label)


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
        """Login bot. On FloodWait: sleep FULL time, then retry. Never exit."""
        while True:
            try:
                await super().start()
                break
            except FloodWait as e:
                wait = int(getattr(e, "value", 0) or 0) + 10
                await _sleep_flood(wait, "bot-login")
                # loop retries after full sleep — do not raise
            except Exception as e:
                logger.error("Bot start failed: %s — retry in 30s", e)
                await asyncio.sleep(30)

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        logger.info(f"🤖 Bot started successfully as @{self.username}")

    async def send_online_log(self, assistants: list | None = None) -> None:
        """One combined ONLINE message (bot + assistants). Throttled 10 min."""
        if not self.logger:
            return
        if not await _should_send_log():
            logger.info("Skipped duplicate start log (Mongo throttle 10 min)")
            return

        lines = [
            "🤖 <b>Tanu Music ONLINE</b>",
            f"• Bot: @{self.username}",
            f"• ID: <code>{self.id}</code>",
            "• Version: 3.0.3",
        ]
        if assistants:
            lines.append("")
            lines.append("<b>Assistants:</b>")
            for i, c in enumerate(assistants, 1):
                uname = getattr(c, "username", None)
                cid = getattr(c, "id", None)
                name = getattr(c, "name", f"Assistant {i}")
                tag = f"@{uname}" if uname else (f"<code>{cid}</code>" if cid else name)
                lines.append(f"• Assistant {i}: {tag}")
        else:
            lines.append("")
            lines.append("⚠️ No assistant connected (set STRING_SESSION)")

        try:
            await self.send_message(self.logger, "\n".join(lines))
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
            logger.error("Log group fail (LOGGER_ID=%s): %s", self.logger, ex)

    async def exit(self) -> None:
        try:
            await super().stop()
        except Exception:
            pass
        logger.info("🤖 Bot client stopped.")
