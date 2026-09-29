import asyncio


class PreloadManager:
    def __init__(self):
        self._tasks = {}

    async def cancel_preload(self, chat_id: int) -> None:
        task = self._tasks.pop(chat_id, None)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except (asyncio.CancelledError, Exception):
                pass

    async def preload_next(self, chat_id: int) -> None:
        import TanuMusic

        queue = TanuMusic.queue
        yt = TanuMusic.yt
        logger = TanuMusic.logger

        items = queue.peek_next(chat_id, count=1)
        if not items:
            return
        item = items[0]
        if getattr(item, "file_path", None):
            return
        vid = getattr(item, "id", None)
        if not vid:
            return

        async def _job():
            try:
                path = await yt.download(vid, video=bool(getattr(item, "video", False)))
                if path:
                    item.file_path = path
            except Exception as e:
                logger.debug(f"preload failed: {e}")

        await self.cancel_preload(chat_id)
        self._tasks[chat_id] = asyncio.create_task(_job())
