class CallQueue:
    def __init__(self, controller):
        self.controller = controller

    async def replay(self, chat_id: int) -> None:
        import TanuMusic

        queue = TanuMusic.queue
        logger = TanuMusic.logger
        media = queue.get_current(chat_id)
        if not media:
            return
        try:
            await self.controller._player.play_media(chat_id, None, media)
        except Exception as e:
            logger.error(f"Replay failed {chat_id}: {e}")

    async def play_next(self, chat_id: int, expected_index: int = None) -> None:
        import TanuMusic

        queue = TanuMusic.queue
        preload = TanuMusic.preload
        logger = TanuMusic.logger

        self.controller._pending_transitions.discard(chat_id)
        try:
            next_item = queue.get_next(chat_id)
            if not next_item:
                await self.controller._controls.stop(chat_id)
                return
            self.controller._track_index[chat_id] = self.controller._track_index.get(chat_id, 0) + 1
            await self.controller._player.play_media(chat_id, None, next_item)
            try:
                await preload.preload_next(chat_id)
            except Exception:
                pass
        except Exception as e:
            logger.error(f"play_next failed {chat_id}: {e}")
            try:
                await self.controller._controls.stop(chat_id)
            except Exception:
                pass

    async def play_previous(self, chat_id: int) -> bool:
        import TanuMusic

        queue = TanuMusic.queue
        prev = queue.get_previous(chat_id)
        if not prev:
            return False
        await self.controller._player.play_media(chat_id, None, prev)
        return True
