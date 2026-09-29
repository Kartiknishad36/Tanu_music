from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class BABY(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="TanuMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        if config.LOGGER_ID:
            try:
                await self.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"<u><b>» {self.mention} bot started :</b></u>\n\n"
                        f"ID : <code>{self.id}</code>\n"
                        f"Name : {self.name}\n"
                        f"Username : @{self.username}"
                    ),
                )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error(
                    "Bot cannot access LOGGER group. Add bot to log group."
                )
            except Exception as ex:
                LOGGER(__name__).error(
                    f"Log group error: {type(ex).__name__}"
                )
            try:
                a = await self.get_chat_member(config.LOGGER_ID, self.id)
                if a.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).warning(
                        "Promote bot as admin in LOGGER group."
                    )
            except Exception:
                pass
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
