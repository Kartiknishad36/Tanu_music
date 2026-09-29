import asyncio
from datetime import datetime

from pyrogram.enums import ChatType

import config
from TanuMusic import app
from TanuMusic.core.call import BABY
from TanuMusic.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT:
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from TanuMusic.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if chat_id not in [
                                config.LOGGER_ID,
                                -1002031903841,
                            ]:
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                    except Exception:
                                        continue
                except Exception:
                    pass


async def auto_end():
    while not await asyncio.sleep(5):
        ender = await is_autoend()
        if not ender:
            continue
        from TanuMusic.utils.database import get_client, is_active_chat

        # placeholder loop – full autoend handled in call.py stream end
        pass


asyncio.create_task(auto_leave())
asyncio.create_task(auto_end())
