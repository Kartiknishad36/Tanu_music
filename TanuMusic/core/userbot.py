from pyrogram import Client

import config
from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="TanuAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1) if config.STRING1 else None,
            no_updates=True,
        )
        self.two = Client(
            name="TanuAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2) if config.STRING2 else None,
            no_updates=True,
        )
        self.three = Client(
            name="TanuAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3) if config.STRING3 else None,
            no_updates=True,
        )
        self.four = Client(
            name="TanuAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4) if config.STRING4 else None,
            no_updates=True,
        )
        self.five = Client(
            name="TanuAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5) if config.STRING5 else None,
            no_updates=True,
        )

    async def _boot(self, client, num: int):
        await client.start()
        me = client.me or await client.get_me()
        # store id on object for older code that uses .id
        object.__setattr__(client, "id", me.id)
        object.__setattr__(client, "name", me.mention or me.first_name)
        object.__setattr__(client, "username", me.username)
        assistants.append(num)
        assistantids.append(me.id)
        try:
            await client.send_message(
                config.LOGGER_ID,
                f"Assistant {num} Started as {me.mention}",
            )
        except Exception:
            LOGGER(__name__).warning(
                f"Assistant {num} cannot access LOGGER group. Add assistant to log group."
            )
        LOGGER(__name__).info(f"Assistant {num} Started as {me.mention}")

    async def start(self):
        LOGGER(__name__).info("Starting assistants...")
        if config.STRING1:
            await self._boot(self.one, 1)
        if config.STRING2:
            await self._boot(self.two, 2)
        if config.STRING3:
            await self._boot(self.three, 3)
        if config.STRING4:
            await self._boot(self.four, 4)
        if config.STRING5:
            await self._boot(self.five, 5)
        if not assistants:
            LOGGER(__name__).error(
                "No STRING_SESSION found. Assistant will not work. Set STRING_SESSION in Railway."
            )

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for c in (self.one, self.two, self.three, self.four, self.five):
            try:
                if c.is_connected:
                    await c.stop()
            except Exception:
                pass
