import logging
from pyrogram.types import Message
from pytgcalls import exceptions
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from ntgcalls import ConnectionNotFound

from TanuMusic.helpers import Media, Track

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
            log.warning(f"Not in call {chat_id}: {e}")
            try:
                await client.play(chat_id, stream)
            except Exception as e2:
                log.error(f"Play retry failed {chat_id}: {e2}")
                raise
        except Exception as e:
            log.error(f"Play failed {chat_id}: {e}")
            raise
