import socket
import time

import heroku3
from pyrogram import filters

import config
from TanuMusic.core.mongo import mongodb, pymongodb

from .logging import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()
db = {}


def is_heroku():
    host = socket.gethostname().upper()
    return "DYNO" in host or "HEROKU" in host


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Database initialized.")


async def sudo():
    global SUDOERS
    OWNER = getattr(config, "OWNER_ID", 0) or 0
    if OWNER:
        try:
            SUDOERS.add(int(OWNER))
        except Exception:
            pass
    try:
        sudoersdb = mongodb.sudoers
        data = await sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not data else list(data.get("sudoers", []))
        if OWNER and OWNER not in sudoers:
            sudoers.append(int(OWNER))
            await sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
        for user_id in sudoers:
            try:
                SUDOERS.add(int(user_id))
            except Exception:
                pass
    except Exception:
        # fallback sync pymongo if async fails
        try:
            users = pymongodb.sudoers.find_one({"sudo": "sudo"})
            if users:
                for i in users.get("sudoers", []):
                    SUDOERS.add(int(i))
        except Exception:
            pass
    LOGGER(__name__).info("Sudo users loaded.")


def heroku():
    global HAPP
    if is_heroku():
        if getattr(config, "HEROKU_API_KEY", None) and getattr(config, "HEROKU_APP_NAME", None):
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info("Heroku app detected.")
            except Exception:
                LOGGER(__name__).warning("Heroku not configured properly.")
