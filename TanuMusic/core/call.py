import asyncio
import os
from datetime import datetime, timedelta
from typing import Union

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio, MediumQualityVideo
from pytgcalls.types.stream import StreamAudioEnded

import config
from TanuMusic import LOGGER, YouTube, app
from TanuMusic.misc import db
from TanuMusic.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from TanuMusic.utils.exceptions import AssistantErr
from TanuMusic.utils.formatters import check_duration, seconds_to_min, speed_converter
from TanuMusic.utils.inline.play import stream_markup, telegram_markup
from TanuMusic.utils.stream.autoclear import auto_clean
from TanuMusic.utils.thumbnails import gen_thumb
from strings import get_string

autoend = {}
LOG_CHAT = getattr(config, "LOG_GROUP_ID", getattr(config, "LOGGER_ID", 0))


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="TanuAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)
        self.userbot2 = Client(
            name="TanuAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)
        self.userbot3 = Client(
            name="TanuAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)
        self.userbot4 = Client(
            name="TanuAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)
        self.userbot5 = Client(
            name="TanuAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        try:
            db[chat_id] = []
            await self.clear_queue(chat_id)
        except Exception:
            pass
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    async def clear_queue(self, chat_id: int):
        try:
            if chat_id in db:
                del db[chat_id]
        except Exception:
            pass

    async def skip_stream(
        self, chat_id: int, link: str, video: Union[bool, str] = None, image: Union[bool, str] = None
    ):
        assistant = await group_assistant(self, chat_id)
        if video:
            stream = AudioVideoPiped(
                link,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
            )
        else:
            stream = AudioPiped(link, audio_parameters=HighQualityAudio())
        await assistant.change_stream(chat_id, stream)

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            if check:
                check.pop(0)
        except Exception:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except Exception:
            pass

    async def stream_call(self, link):
        if not LOG_CHAT:
            return
        assistant = await group_assistant(self, LOG_CHAT)
        await assistant.join_group_call(
            LOG_CHAT,
            AudioPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(0.5)
        await assistant.leave_group_call(LOG_CHAT)

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        if video:
            stream = AudioVideoPiped(
                link,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
            )
        else:
            stream = AudioPiped(link, audio_parameters=HighQualityAudio())
        try:
            await assistant.join_group_call(
                chat_id, stream, stream_type=StreamType().pulse_stream
            )
        except NoActiveGroupCall:
            raise AssistantErr(_["call_4"] if "call_4" in _ else "No active voice chat. Start VC first.")
        except AlreadyJoinedError:
            raise AssistantErr(_["call_1"] if "call_1" in _ else "Assistant already in VC.")
        except TelegramServerError:
            raise AssistantErr(_["call_2"] if "call_2" in _ else "Telegram server error. Retry.")
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        try:
            if not check:
                await remove_active_video_chat(chat_id)
                await remove_active_chat(chat_id)
                try:
                    await client.leave_group_call(chat_id)
                except Exception:
                    pass
                return
            loop = await get_loop(chat_id)
            if loop == 0:
                check.pop(0)
            else:
                await set_loop(chat_id, loop - 1)
            if not check:
                await remove_active_video_chat(chat_id)
                await remove_active_chat(chat_id)
                try:
                    await client.leave_group_call(chat_id)
                except Exception:
                    pass
                return
            queued = check[0]["file"]
            streamtype = check[0].get("streamtype", "audio")
            if str(streamtype) == "video":
                stream = AudioVideoPiped(
                    queued,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=MediumQualityVideo(),
                )
            else:
                stream = AudioPiped(queued, audio_parameters=HighQualityAudio())
            await client.change_stream(chat_id, stream)
        except Exception:
            try:
                await remove_active_video_chat(chat_id)
                await remove_active_chat(chat_id)
                await client.leave_group_call(chat_id)
            except Exception:
                pass

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
        @self.one.on_kicked()
        @self.two.on_kicked()
        @self.three.on_kicked()
        @self.four.on_kicked()
        @self.five.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.two.on_closed_voice_chat()
        @self.three.on_closed_voice_chat()
        @self.four.on_closed_voice_chat()
        @self.five.on_closed_voice_chat()
        @self.one.on_left()
        @self.two.on_left()
        @self.three.on_left()
        @self.four.on_left()
        @self.five.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        @self.four.on_stream_end()
        @self.five.on_stream_end()
        async def stream_end_handler(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(client, update.chat_id)


BABY = Call()
