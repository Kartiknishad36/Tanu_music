from random import randint
from time import time
import asyncio
import logging

from pymongo import AsyncMongoClient

from TanuMusic import config, logger, userbot


class MongoBackgroundFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        return not (
            "MongoClient background task encountered an error" in msg
            or ("AutoReconnect" in msg and "background task" in msg)
            or ("_OperationCancelled" in msg and "background task" in msg)
        )


logging.getLogger("pymongo.client").addFilter(MongoBackgroundFilter())


class MongoDB:
    def __init__(self):
        self.mongo = AsyncMongoClient(
            config.MONGO_URL,
            serverSelectionTimeoutMS=12500,
            connectTimeoutMS=20000,
            socketTimeoutMS=20000,
            maxPoolSize=20,
            minPoolSize=5,
            maxIdleTimeMS=30000,
            waitQueueTimeoutMS=10000,
            retryWrites=True,
            retryReads=True,
        )
        self.db = self.mongo.TanuTune

        self.admin_list = {}
        self.admin_cache_time = {}
        self.active_calls = {}
        self.blacklisted = []
        self.notified = []
        self.cache = self.db.cache
        self.logger = False
        self.vplay_enabled = None

        self.assistant = {}
        self.assistantdb = self.db.assistant

        self.auth = {}
        self.authdb = self.db.auth

        self.chats = []
        self.chatsdb = self.db.chats

        self.lang = {}
        self.langdb = self.db.lang

        self.play_mode = []
        self.playmodedb = self.db.play

        self.users = []
        self.usersdb = self.db.users

        # /sg name-username-bio-photo history
        self.historydb = self.db.user_history

    async def connect(self) -> None:
        max_retries = 3
        retry_delay = 5
        for attempt in range(1, max_retries + 1):
            try:
                start = time()
                await self.mongo.admin.command("ping")
                logger.info(f"Database connection successful. ({time() - start:.2f}s)")
                await self.authdb.create_index("_id")
                await self.langdb.create_index("_id")
                await self.cache.create_index("_id")
                try:
                    await self.historydb.create_index("_id")
                except Exception:
                    pass
                await self.load_cache()
                return
            except Exception as e:
                if attempt < max_retries:
                    wait_time = retry_delay * (2 ** (attempt - 1))
                    logger.warning(
                        f"DB connect attempt {attempt}/{max_retries} failed: {type(e).__name__}. Retry in {wait_time}s..."
                    )
                    await asyncio.sleep(wait_time)
                else:
                    raise SystemExit(
                        f"Database connection failed after {max_retries} attempts: {e}"
                    )

    async def close(self) -> None:
        try:
            await self.mongo.close()
            logger.info("Database connection closed.")
        except Exception as e:
            logger.warning(f"Error closing DB: {e}")

    async def get_call(self, chat_id: int):
        return self.active_calls.get(chat_id)

    async def add_call(self, chat_id: int) -> None:
        self.active_calls[chat_id] = {"playing": True}

    async def remove_call(self, chat_id: int) -> None:
        self.active_calls.pop(chat_id, None)

    async def playing(self, chat_id: int, paused: bool | None = None) -> bool:
        if chat_id not in self.active_calls:
            return False
        if paused is not None:
            self.active_calls[chat_id]["playing"] = not paused
        return bool(self.active_calls[chat_id].get("playing", False))

    async def get_admins(self, chat_id: int, reload: bool = False) -> list:
        from TanuMusic.helpers import reload_admins

        current_time = time()
        if (
            not reload
            and chat_id in self.admin_list
            and current_time - self.admin_cache_time.get(chat_id, 0) < 300
        ):
            return self.admin_list[chat_id]

        try:
            admins = await reload_admins(chat_id)
        except Exception:
            admins = self.admin_list.get(chat_id, [])
        self.admin_list[chat_id] = admins
        self.admin_cache_time[chat_id] = current_time
        return admins

    async def _get_auth(self, chat_id: int) -> set:
        if chat_id not in self.auth:
            doc = await self.authdb.find_one({"_id": chat_id}) or {}
            self.auth[chat_id] = set(doc.get("user_ids", []))
        return self.auth[chat_id]

    async def is_auth(self, chat_id: int, user_id: int) -> bool:
        return user_id in await self._get_auth(chat_id)

    async def add_auth(self, chat_id: int, user_id: int) -> None:
        users = await self._get_auth(chat_id)
        if user_id not in users:
            users.add(user_id)
            await self.authdb.update_one(
                {"_id": chat_id}, {"$addToSet": {"user_ids": user_id}}, upsert=True
            )

    async def rm_auth(self, chat_id: int, user_id: int) -> None:
        users = await self._get_auth(chat_id)
        if user_id in users:
            users.discard(user_id)
            await self.authdb.update_one(
                {"_id": chat_id}, {"$pull": {"user_ids": user_id}}
            )

    async def set_assistant(self, chat_id: int) -> int:
        num = randint(1, max(1, len(userbot.clients)))
        await self.assistantdb.update_one(
            {"_id": chat_id}, {"$set": {"num": num}}, upsert=True
        )
        self.assistant[chat_id] = num
        return num

    async def get_assistant(self, chat_id: int):
        from TanuMusic import tune

        if chat_id not in self.assistant:
            doc = await self.assistantdb.find_one({"_id": chat_id})
            num = doc["num"] if doc else await self.set_assistant(chat_id)
            self.assistant[chat_id] = num

        if not userbot.clients:
            raise RuntimeError("No assistant clients available")

        if self.assistant[chat_id] > len(userbot.clients):
            await self.set_assistant(chat_id)

        return tune.clients[self.assistant[chat_id] - 1]

    async def get_client(self, chat_id: int):
        return await self.get_assistant(chat_id)

    async def add_blacklist(self, chat_id: int) -> None:
        if chat_id not in self.blacklisted:
            self.blacklisted.append(chat_id)
            await self.cache.update_one(
                {"_id": "blacklist"},
                {"$addToSet": {"ids": chat_id}},
                upsert=True,
            )

    async def del_blacklist(self, chat_id: int) -> None:
        if chat_id in self.blacklisted:
            self.blacklisted.remove(chat_id)
            await self.cache.update_one(
                {"_id": "blacklist"}, {"$pull": {"ids": chat_id}}
            )

    async def get_blacklisted(self, chat: bool = False) -> list:
        if not self.blacklisted:
            doc = await self.cache.find_one({"_id": "blacklist"})
            if doc:
                self.blacklisted = list(doc.get("ids", []))
        return self.blacklisted

    async def is_chat(self, chat_id: int) -> bool:
        return chat_id in self.chats

    async def add_chat(self, chat_id: int) -> None:
        if chat_id not in self.chats:
            self.chats.append(chat_id)
            await self.chatsdb.update_one(
                {"_id": chat_id}, {"$set": {"_id": chat_id}}, upsert=True
            )

    async def rm_chat(self, chat_id: int) -> None:
        if chat_id in self.chats:
            self.chats.remove(chat_id)
            await self.chatsdb.delete_one({"_id": chat_id})

    async def get_chats(self) -> list:
        if not self.chats:
            self.chats = [c["_id"] async for c in self.chatsdb.find()]
        return self.chats

    async def set_lang(self, chat_id: int, lang_code: str) -> None:
        self.lang[chat_id] = lang_code
        await self.langdb.update_one(
            {"_id": chat_id}, {"$set": {"lang": lang_code}}, upsert=True
        )

    async def get_lang(self, chat_id: int) -> str:
        if chat_id not in self.lang:
            doc = await self.langdb.find_one({"_id": chat_id})
            self.lang[chat_id] = doc.get("lang", "en") if doc else "en"
        return self.lang[chat_id]

    async def get_vplay_enabled(self) -> bool:
        if self.vplay_enabled is None:
            doc = await self.cache.find_one({"_id": "vplay"})
            self.vplay_enabled = doc.get("enabled", True) if doc else True
        return self.vplay_enabled

    async def set_vplay_enabled(self, enabled: bool) -> None:
        self.vplay_enabled = enabled
        await self.cache.update_one(
            {"_id": "vplay"}, {"$set": {"enabled": enabled}}, upsert=True
        )

    async def is_logger(self) -> bool:
        return await self.get_logger()

    async def get_logger(self) -> bool:
        doc = await self.cache.find_one({"_id": "logger"})
        if doc:
            self.logger = doc.get("status", False)
        return self.logger

    async def set_logger(self, status: bool) -> None:
        self.logger = status
        await self.cache.update_one(
            {"_id": "logger"}, {"$set": {"status": status}}, upsert=True
        )

    async def get_autoleave(self, chat_id: int) -> bool:
        doc = await self.cache.find_one({"_id": f"autoleave_{chat_id}"})
        return doc.get("enabled", False) if doc else False

    async def set_autoleave(self, chat_id: int, enabled: bool) -> None:
        await self.cache.update_one(
            {"_id": f"autoleave_{chat_id}"},
            {"$set": {"enabled": enabled}},
            upsert=True,
        )

    async def get_loop(self, chat_id: int) -> int:
        doc = await self.cache.find_one({"_id": f"loop_{chat_id}"})
        return doc.get("mode", 0) if doc else 0

    async def set_loop(self, chat_id: int, mode: int) -> None:
        await self.cache.update_one(
            {"_id": f"loop_{chat_id}"},
            {"$set": {"mode": mode}},
            upsert=True,
        )

    async def get_play_mode(self, chat_id: int) -> bool:
        if chat_id not in self.play_mode:
            doc = await self.playmodedb.find_one({"_id": chat_id})
            if doc:
                self.play_mode.append(chat_id)
        return chat_id in self.play_mode

    async def set_play_mode(self, chat_id: int, remove: bool = False) -> None:
        if remove:
            if chat_id in self.play_mode:
                self.play_mode.remove(chat_id)
            await self.playmodedb.delete_one({"_id": chat_id})
        else:
            if chat_id not in self.play_mode:
                self.play_mode.append(chat_id)
            await self.playmodedb.update_one(
                {"_id": chat_id}, {"$set": {"_id": chat_id}}, upsert=True
            )

    async def add_sudo(self, user_id: int) -> None:
        await self.cache.update_one(
            {"_id": "sudoers"}, {"$addToSet": {"user_ids": user_id}}, upsert=True
        )

    async def del_sudo(self, user_id: int) -> None:
        await self.cache.update_one(
            {"_id": "sudoers"}, {"$pull": {"user_ids": user_id}}
        )

    async def get_sudoers(self) -> list:
        doc = await self.cache.find_one({"_id": "sudoers"})
        return doc.get("user_ids", []) if doc else []

    async def is_user(self, user_id: int) -> bool:
        return user_id in self.users

    async def add_user(self, user_id: int) -> None:
        if not await self.is_user(user_id):
            self.users.append(user_id)
            await self.usersdb.update_one(
                {"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True
            )

    async def rm_user(self, user_id: int) -> None:
        if await self.is_user(user_id):
            self.users.remove(user_id)
            await self.usersdb.delete_one({"_id": user_id})

    async def get_users(self) -> list:
        if not self.users:
            self.users = [user["_id"] async for user in self.usersdb.find()]
        return self.users

    async def load_cache(self) -> None:
        logger.info("Loading database cache...")
        await self.get_chats()
        await self.get_users()
        await self.get_blacklisted(chat=True)
        await self.get_logger()
        await self.get_vplay_enabled()
        await self.get_sudoers()
        logger.info(
            f"Cache loaded: {len(self.chats)} chats, {len(self.users)} users, {len(self.blacklisted)} blacklisted."
        )
