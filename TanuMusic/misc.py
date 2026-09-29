import socket
import time

import heroku3
from pyrogram import filters

import config
from TanuMusic.core.mongo import pymongodb

from .logging import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "DYNO" in socket.gethostname().upper() or "HEROKU" in socket.gethostname().upper()


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Database initialized.")


def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    if OWNER:
        SUDOERS = filters.user(OWNER)
        SUDOERS.add(OWNER)
    try:
        users = pymongodb.sudoers.find_one({"sudo": "sudo"})
        if users:
            for i in users["sudoers"]:
                SUDOERS.add(int(i))
    except Exception:
        pass
    LOGGER(__name__).info("Sudo users loaded.")


def heroku():
    global HAPP
    if is_heroku():
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info("Heroku app detected.")
            except Exception:
                LOGGER(__name__).warning("Heroku not configured properly.")
