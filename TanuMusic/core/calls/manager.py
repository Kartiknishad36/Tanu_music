import asyncio
from ntgcalls import ConnectionNotFound, TelegramServerError
from pytgcalls import PyTgCalls, exceptions, types
from pytgcalls.pytgcalls_session import PyTgCallsSession
from TanuMusic import logger
import TanuMusic

class CallsManager:
    def __init__(self, controller):
        self.controller = controller

    async def boot(self) -> None:
        PyTgCallsSession.notice_displayed = True
        # Fresh userbot lo - __init__.py wala None nahi
        userbot = TanuMusic.userbot
        if not userbot:
            from TanuMusic import userbot as ub
            userbot = ub
        
        for ub in userbot.clients:
            client = PyTgCalls(ub, cache_duration=100)
            await client.start()
            self.controller.clients.append(client)
            await self.decorators(client)
        logger.info("PyTgCalls client(s) started.")

    async def ping(self) -> float:
        if not self.controller.clients:
            return 0.0
        pings = [client.ping for client in self.controller.clients]
        return round(sum(pings) / len(pings), 2)

    async def decorators(self, client: PyTgCalls) -> None:
        @client.on_update()
        async def update_handler(_, update: types.Update) -> None:
            try:
                if isinstance(update, types.StreamEnded):
                    if update.stream_type == types.StreamEnded.Type.AUDIO:
                        chat_id = update.chat_id
                        expected_index = self.controller._track_index.get(chat_id, 0)
                        if chat_id not in self.controller._pending_transitions:
                            self.controller._pending_transitions.add(chat_id)
                            asyncio.create_task(
                                self.controller._queue.play_next(chat_id, expected_index)
                            )
                elif isinstance(update, types.ChatUpdate):
                    if update.status in [
                        types.ChatUpdate.Status.KICKED,
                        types.ChatUpdate.Status.LEFT_GROUP,
                        types.ChatUpdate.Status.CLOSED_VOICE_CHAT,
                    ]:
                        await self.controller._controls.stop(update.chat_id)
            except (ConnectionNotFound, exceptions.NotInCallError, TelegramServerError):
                return
            except Exception as e:
                logger.debug(f"Ignoring update handler error: {e}")
