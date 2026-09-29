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


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="TanuAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
        self.userbot2 = Client(
            name="TanuAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        )
        self.userbot3 = Client(
            name="TanuAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        )
        self.userbot4 = Client(
            name="TanuAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(
            self.userbot4,
            cache_duration=100,
        )
        self.userbot5 = Client(
            name="TanuAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(
            self.userbot5,
            cache_duration=100,
        )

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
        except:
            pass
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def clear_queue(self, chat_id: int):
        try:
            if chat_id in db:
                del db[chat_id]
        except:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
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
        await assistant.change_stream(
            chat_id,
            stream,
        )

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            if check:
                check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def seek_stream(self, chat_id, file_path, duration, to_seek, video):
        assistant = await group_assistant(self, chat_id)
        if video:
            stream = AudioVideoPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
                video_parameters=MediumQualityVideo(),
                additional_ffmpeg_parameters={
                    "before_options": f"-ss {to_seek}",
                    "options": f"-t {duration}",
                },
            )
        else:
            stream = AudioPiped(
                file_path,
                audio_parameters=HighQualityAudio(),
                additional_ffmpeg_parameters={
                    "before_options": f"-ss {to_seek}",
                    "options": f"-t {duration}",
                },
            )
        await assistant.change_stream(chat_id, stream)

    async def speedup_stream(self, chat_id, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)
        if int(speed) != int(100):
            base = 1.0 if int(speed) == 100 else float(speed) / 100.0
            _file = file_path
            if not playing["streamtype"] == "index":
                _file = await YouTube.download(file_path, mystic=None, video=playing["video"])
            _duration = await check_duration(_file)
            _duration = int(_duration)
            _sec = speed_converter(_duration, base)
            if playing["video"]:
                stream = AudioVideoPiped(
                    _file,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=MediumQualityVideo(),
                    additional_ffmpeg_parameters={
                        "before_options": f"-filter:a atempo={base}",
                        "options": f"-t {_sec}",
                    },
                )
            else:
                stream = AudioPiped(
                    _file,
                    audio_parameters=HighQualityAudio(),
                    additional_ffmpeg_parameters={
                        "before_options": f"-filter:a atempo={base}",
                        "options": f"-t {_sec}",
                    },
                )
            await assistant.change_stream(chat_id, stream)
        else:
            if playing["video"]:
                stream = AudioVideoPiped(
                    file_path,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=MediumQualityVideo(),
                )
            else:
                stream = AudioPiped(file_path, audio_parameters=HighQualityAudio())
            await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.join_group_call(
            config.LOG_GROUP_ID,
            AudioPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(0.5)
        await assistant.leave_group_call(config.LOG_GROUP_ID)

    async def join_assistant(self, original_chat_id, chat_id):
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        assistant = await group_assistant(self, chat_id)
        try:
            try:
                await assistant.join_group_call(
                    chat_id,
                    AudioPiped("http://docs.evostream.com/sample_content/sintel_trailer.mp4"),
                    stream_type=StreamType().pulse_stream,
                )
            except AlreadyJoinedError:
                raise AssistantErr(_["call_1"])
            except TelegramServerError:
                raise AssistantErr(_["call_2"])
            except NoActiveGroupCall:
                try:
                    await app.promote_chat_member(
                        chat_id,
                        (await assistant.get_me()).id,
                        can_manage_voice_chats=True,
                    )
                except Exception:
                    raise AssistantErr(_["call_3"])
                raise AssistantErr(_["call_4"])
        except Exception as e:
            if "already" in str(e).lower() or "joined" in str(e).lower():
                pass
            else:
                raise AssistantErr(f"Assistant join error: {e}")

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
            stream = (
                AudioVideoPiped(
                    link,
                    audio_parameters=HighQualityAudio(),
                    video_parameters=MediumQualityVideo(),
                )
                if await is_autoend()
                else AudioPiped(link, audio_parameters=HighQualityAudio())
            )
        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                raise e
            try:
                await assistant.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
            except Exception as e:
                raise AssistantErr(
                    _["call_3"] if "not found" in str(e).lower() else str(e)
                )
        except AlreadyJoinedError:
            raise AssistantErr(_["call_1"])
        except TelegramServerError:
            raise AssistantErr(_["call_2"])
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            clock_time = datetime.now() + timedelta(minutes=1)
            autoend[chat_id] = clock_time

    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            if popped:
                await auto_clean(popped)
            if not check:
                await auto_clean(check)
                await remove_active_video_chat(chat_id)
                await remove_active_chat(chat_id)
                try:
                    await client.leave_group_call(chat_id)
                except:
                    pass
                return
        except:
            try:
                await remove_active_video_chat(chat_id)
                await remove_active_chat(chat_id)
                await client.leave_group_call(chat_id)
            except:
                pass
            return
        queued = check[0]["file"]
        language = await get_lang(chat_id)
        _ = get_string(language)
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        streamtype = check[0]["streamtype"]
        audio_stream_quality = await config.audio_bitrate()
        video_stream_quality = await config.video_bitrate()
        videoid = check[0]["vidid"]
        user_id = check[0]["user_id"]
        check[0]["played"] = 0
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            if streamtype == "video":
                stream = AudioVideoPiped(
                    link,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
            else:
                stream = AudioPiped(
                    link,
                    audio_parameters=audio_stream_quality,
                )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            img = await gen_thumb(videoid, user_id)
            button = telegram_markup(_)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "vid_" in queued:
            mystic = await app.send_message(original_chat_id, _["call_7"])
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=True if str(streamtype) == "video" else False,
                )
            except:
                return await mystic.edit_text(
                    _["call_6"], disable_web_page_preview=True
                )
            if str(streamtype) == "video":
                stream = AudioVideoPiped(
                    file_path,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
            else:
                stream = AudioPiped(
                    file_path,
                    audio_parameters=audio_stream_quality,
                )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            img = await gen_thumb(videoid, user_id)
            button = stream_markup(_, videoid)
            await mystic.delete()
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    check[0]["dur"],
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
        elif "index_" in queued:
            file = check[0]["file"]
            if str(streamtype) == "video":
                stream = AudioVideoPiped(
                    file,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
            else:
                stream = AudioPiped(
                    file,
                    audio_parameters=audio_stream_quality,
                )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            button = telegram_markup(_)
            run = await app.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            if str(streamtype) == "video":
                stream = AudioVideoPiped(
                    queued,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
            else:
                stream = AudioPiped(
                    queued,
                    audio_parameters=audio_stream_quality,
                )
            try:
                await client.change_stream(chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            if videoid == "telegram":
                button = telegram_markup(_)
                run = await app.send_photo(
                    original_chat_id,
                    photo=config.TELEGRAM_AUDIO_URL
                    if str(streamtype) == "audio"
                    else config.TELEGRAM_VIDEO_URL,
                    caption=_["stream_1"].format(
                        title[:27], "Telegram",
                        check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_)
                run = await app.send_photo(
                    original_chat_id,
                    photo=config.SOUNCLOUD_IMG_URL,
                    caption=_["stream_1"].format(
                        title[:27], "SoundCloud",
                        check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                img = await gen_thumb(videoid, user_id)
                button = stream_markup(_, videoid)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        if config.STRING4:
            pings.append(await self.four.ping)
        if config.STRING5:
            pings.append(await self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client\n")
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


Call = Call()
