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

        log_id = getattr(config, "LOGGER_ID", 0) or getattr(config, "LOG_GROUP_ID", 0) or 0
        try:
            log_id = int(log_id)
        except Exception:
            log_id = 0

        if not log_id:
            LOGGER(__name__).error(
                "LOGGER_ID not set in Railway variables. "
                "Set LOGGER_ID=-100xxxxxxxxxx and add bot as admin in that group."
            )
        else:
            try:
                await self.send_message(
                    chat_id=log_id,
                    text=(
                        f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\n"
                        f"ɪᴅ : <code>{self.id}</code>\n"
                        f"ɴᴀᴍᴇ : {self.name}\n"
                        f"ᴜsᴇʀɴᴀᴍᴇ : @{self.username}\n\n"
                        f"✅ <b>Tanu Music is online</b>"
                    ),
                    parse_mode=ParseMode.HTML,
                )
                LOGGER(__name__).info(f"Start message sent to log group {log_id}")
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error(
                    f"Bot cannot access log group {log_id}. "
                    "Add the bot to the log group and promote as admin."
                )
            except errors.UserNotParticipant:
                LOGGER(__name__).error(
                    f"Bot is not a member of log group {log_id}. Add bot first."
                )
            except Exception as ex:
                LOGGER(__name__).error(
                    f"Log group error ({log_id}): {type(ex).__name__}: {ex}"
                )
            try:
                a = await self.get_chat_member(log_id, self.id)
                if a.status not in (
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.OWNER,
                ):
                    LOGGER(__name__).warning(
                        "Promote bot as admin in LOGGER group for full features."
                    )
            except Exception:
                pass

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
