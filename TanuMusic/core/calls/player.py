import logging
from pyrogram.types import Message
from pytgcalls import exceptions
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from ntgcalls import ConnectionNotFound

from TanuMusic.helpers import Media, Track
from TanuMusic.helpers.assistant_join import ensure_assistant_in_chat

log = logging.getLogger(__name__)


class CallPlayer:
    def __init__(self, controller):
        self.controller = controller

    async def play_media(
        self,
        chat_id: int,
        message: Message | None,
        media: Media | Track,
        seek_time: int = 0,
    ) -> None:
        async with self.controller.get_lock(chat_id):
            await self._play_media_impl(chat_id, message, media, seek_time)

    async def _play_media_impl(
        self,
        chat_id: int,
        message: Message | None,
        media: Media | Track,
        seek_time: int = 0,
    ) -> None:
        import TanuMusic

        db = TanuMusic.db

        # Must be in group first — fixes CHANNEL_INVALID
        ok, reason = await ensure_assistant_in_chat(chat_id)
        if not ok:
            log.error(f"Assistant not in chat {chat_id}: {reason}")
            if message:
                try:
                    await message.edit_text(reason)
                except Exception:
                    pass
            raise RuntimeError(reason)

        client = await db.get_assistant(chat_id)
        file_path = getattr(media, "file_path", None)
        if not file_path:
            log.error(f"No file_path for media in {chat_id}")
            return

        video = bool(getattr(media, "video", False))
        try:
            if video:
                stream = MediaStream(
                    file_path,
                    audio_parameters=AudioQuality.STUDIO,
                    video_parameters=VideoQuality.SD_480p,
                )
            else:
                stream = MediaStream(
                    file_path,
                    audio_parameters=AudioQuality.STUDIO,
                    video_flags=MediaStream.Flags.IGNORE,
                )

            await client.play(chat_id, stream)
            await db.playing(chat_id, paused=False)
            if chat_id not in db.active_calls:
                await db.add_call(chat_id)
            log.info(f"Playing in {chat_id}: {getattr(media, 'title', file_path)}")
        except (ConnectionNotFound, exceptions.NotInCallError) as e:
            log.warning(f"Not in call {chat_id}: {e} — retry after join")
            ok2, reason2 = await ensure_assistant_in_chat(chat_id)
            if not ok2:
                raise RuntimeError(reason2)
            try:
                await client.play(chat_id, stream)
                await db.playing(chat_id, paused=False)
                if chat_id not in db.active_calls:
                    await db.add_call(chat_id)
            except Exception as e2:
                log.error(f"Play retry failed {chat_id}: {e2}")
                raise
        except Exception as e:
            err = str(e)
            if "CHANNEL_INVALID" in err or "CHANNEL_PRIVATE" in err:
                ok3, reason3 = await ensure_assistant_in_chat(chat_id)
                if ok3:
                    try:
                        await client.play(chat_id, stream)
                        await db.playing(chat_id, paused=False)
                        if chat_id not in db.active_calls:
                            await db.add_call(chat_id)
                        return
                    except Exception as e3:
                        log.error(f"Play after rejoin failed: {e3}")
                        raise RuntimeError(
                            "❌ Assistant group join ke baad bhi VC fail.\n"
                            "• VC start karo (group me video chat on)\n"
                            "• Assistant ko manually group me add karke /play do"
                        ) from e3
                raise RuntimeError(reason3) from e
            log.error(f"Play failed {chat_id}: {e}")
            raise
