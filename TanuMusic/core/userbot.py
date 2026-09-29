import asyncio

from pyrogram import Client
from pyrogram.errors import FloodWait

from TanuMusic import config, logger


async def _sleep_flood(wait: int, label: str) -> None:
    wait = max(int(wait), 5)
    logger.error(
        "⏳ FloodWait %s: %s sec (~%s min). Do NOT redeploy.",
        label,
        wait,
        max(1, wait // 60),
    )
    remaining = wait
    while remaining > 0:
        step = min(60, remaining)
        await asyncio.sleep(step)
        remaining -= step
        if remaining > 0:
            logger.info("⏳ %s: %ss left...", label, remaining)
    logger.info("✅ FloodWait %s done — retry", label)


class Userbot:
    """Assistant manager — only sessions with non-empty STRING_SESSION."""

    def __init__(self):
        self.clients = []
        self.one = None
        self.two = None
        self.three = None

        mapping = [
            ("one", "SESSION1", 1),
            ("two", "SESSION2", 2),
            ("three", "SESSION3", 3),
        ]
        for attr, key, num in mapping:
            session = (getattr(config, key, None) or "").strip()
            if not session:
                continue
            client = Client(
                name=f"TanuTuneUB{num}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=session,
                in_memory=True,
            )
            setattr(self, attr, client)

    async def boot_client(self, num: int, client: Client):
        if client is None:
            return

        while True:
            try:
                await client.start()
                break
            except FloodWait as e:
                wait = int(getattr(e, "value", 0) or 0) + 10
                await _sleep_flood(wait, f"assistant-{num}")
            except Exception as e:
                logger.error(f"Assistant {num} failed to start: {e}")
                return

        client.id = client.me.id if client.me else None
        client.name = client.me.first_name if client.me else f"Assistant{num}"
        client.username = client.me.username if client.me else None
        client.mention = client.me.mention if client.me else client.name
        self.clients.append(client)
        logger.info(
            f"Assistant {num} started as @{client.username or client.id}"
        )

        try:
            from TanuMusic import app

            if app.logger:
                uname = f"@{client.username}" if client.username else str(client.id)
                await app.send_message(
                    app.logger,
                    f"🎧 <b>Assistant {num} Started</b>\n• {uname}\n• ID: <code>{client.id}</code>",
                )
        except Exception as e:
            logger.warning(f"Assistant {num} log msg failed: {e}")

    async def boot(self):
        if self.one:
            await self.boot_client(1, self.one)
        if self.two:
            await self.boot_client(2, self.two)
        if self.three:
            await self.boot_client(3, self.three)

        if not self.clients:
            logger.warning("No assistant clients — set STRING_SESSION")

    async def exit(self):
        for client in list(self.clients):
            try:
                if client and getattr(client, "is_connected", False):
                    await client.stop()
            except Exception as e:
                logger.warning(f"Error stopping assistant: {e}")
        self.clients.clear()
        logger.info("Assistants stopped.")
