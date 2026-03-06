import socket
import time

import heroku3
from pyrogram import filters

import config
from IMMORTAL_MUSIC.core.mongo import mongodb

from .logger import LOGGER

SUDOERS = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "master",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("DATABASE LOAD DONE")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info("SUDO USER LOAD DONE")


def heroku():
    global HAPP
    if is_heroku:
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info(f"ðŸŸð—›ð—˜ð—¥ð—¢ð—žð—¨ ð—”ð—£ð—£ ð—¡ð—”ð— ð—˜ ð—Ÿð—¢ð—”ð——......ðŸ’¦..")
            except BaseException:
                LOGGER(__name__).warning(
                    f"ðŸ“ð˜ð¨ð® ð‡ðšð¯ðž ðð¨ð­ ð…ð¢ð¥ð¥ðžð ð‡ðžð«ð¨ð¤ð® ð€ð©ð¢ ðŠðžð² ð€ð§ð ð‡ðžð«ð¨ð¤ð® ð€ð©ð© ððšð¦ðž ðŸ•Šï¸ð‚ð¨ð«ð«ðžðœð­...."
                )

