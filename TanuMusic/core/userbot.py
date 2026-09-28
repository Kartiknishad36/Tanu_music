# ===============================================================================
# userbot.py - Assistant/Userbot Client Manager
# ===============================================================================
from pyrogram import Client

from TanuMusic import config, logger


class Userbot(Client):
    def __init__(self):
        self.clients = []
        clients = {"one": "SESSION1", "two": "SESSION2", "three": "SESSION3"}

        for key, string_key in clients.items():
            name = f"TanuTuneUB{key[-1]}"
            session = getattr(config, string_key)
            setattr(
                self,
                key,
                Client(
                    name=name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=session,
                ),
            )

    async def boot_client(self, num: int, ub: Client):
        clients = {1: self.one, 2: self.two, 3: self.three}
        client = clients[num]
        try:
            await client.start()
        except Exception as e:
            logger.error(f"Assistant {num} failed to start: {e}")
            return

        try:
            await client.send_message(config.LOGGER_ID, f"Assistant {num} Started")
        except Exception as e:
            logger.warning(f"Assistant {num} couldn't send to logger: {e}")

        client.id = client.me.id if hasattr(client, "me") and client.me else None
        client.name = (
            client.me.first_name
            if hasattr(client, "me") and client.me
            else f"Assistant{num}"
        )
        client.username = (
            client.me.username if hasattr(client, "me") and client.me else None
        )
        client.mention = (
            client.me.mention
            if hasattr(client, "me") and client.me
            else client.name
        )
        self.clients.append(client)
        logger.info(f"Assistant {num} started as @{client.username}")

    async def boot(self):
        if config.SESSION1:
            await self.boot_client(1, self.one)
        if config.SESSION2:
            await self.boot_client(2, self.two)
        if config.SESSION3:
            await self.boot_client(3, self.three)

    async def exit(self):
        try:
            if config.SESSION1 and hasattr(self.one, "is_connected") and self.one.is_connected:
                await self.one.stop()
        except Exception as e:
            logger.warning(f"Error stopping assistant 1: {e}")
        try:
            if config.SESSION2 and hasattr(self.two, "is_connected") and self.two.is_connected:
                await self.two.stop()
        except Exception as e:
            logger.warning(f"Error stopping assistant 2: {e}")
        try:
            if config.SESSION3 and hasattr(self.three, "is_connected") and self.three.is_connected:
                await self.three.stop()
        except Exception as e:
            logger.warning(f"Error stopping assistant 3: {e}")
        logger.info("Assistants stopped.")
