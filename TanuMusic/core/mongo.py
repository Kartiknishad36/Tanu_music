from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import config
from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://tmp:tmp@cluster0.mongodb.net/tmp"


try:
    LOGGER(__name__).info("Connecting to your Mongo Database...")
    if config.MONGO_DB_URI is None:
        raise Exception("MONGO_DB_URI not set")
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    mongodb = _mongo_async_.Tanu
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    pymongodb = _mongo_sync_.Tanu
except Exception:
    LOGGER(__name__).error("Failed to connect MongoDB. Check MONGO_DB_URI.")
    exit()
