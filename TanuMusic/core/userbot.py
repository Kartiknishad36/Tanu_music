from pyrogram import Client
from pyrogram.errors import FloodWait

from TanuMusic import config, logger


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
        try:
            await client.start()
        except FloodWait as e:
            logger.error(f"Assistant {num} FloodWait {e.value}s — skip this start")
            return
        except Exception as e:
            logger.error(f"Assistant {num} failed to start: {e}")
            return

        client.id = client.me.id if client.me else None
        client.name = (
            client.me.first_name if client.me else f"Assistant{num}"
        )
        client.username = client.me.username if client.me else None
        client.mention = client.me.mention if client.me else client.name
        self.clients.append(client)
        logger.info(
            f"Assistant {num} started as @{client.username or client.id}"
        )
        # No log-group message here — bot sends one combined ONLINE msg

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
