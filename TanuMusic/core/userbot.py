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

    async def start(self):
        LOGGER(__name__).info("Starting assistants...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.send_message(config.LOGGER_ID, "Assistant 1 Started")
            except Exception:
                LOGGER(__name__).warning("Assistant 1 cannot access LOGGER group.")
            assistants.append(1)
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant 1 Started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Assistant 2 Started")
            except Exception:
                pass
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)

        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Assistant 3 Started")
            except Exception:
                pass
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)

        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)

        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except Exception:
            pass
