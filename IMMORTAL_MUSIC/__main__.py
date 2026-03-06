import os
import sys
import asyncio
import importlib

from pyrogram import idle
from pyrogram import utils as pyrogram_utils

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from IMMORTAL_MUSIC import LOGGER, app, userbot
from IMMORTAL_MUSIC.core.call import NOBITA
from IMMORTAL_MUSIC.misc import sudo
from IMMORTAL_MUSIC.plugins import ALL_MODULES
from IMMORTAL_MUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # Telegram channel IDs can exceed Pyrogram's legacy 32-bit channel range.
    # Expand accepted range to prevent "Peer id invalid" on large channel updates.
    if pyrogram_utils.MIN_CHANNEL_ID > -1009999999999:
        pyrogram_utils.MIN_CHANNEL_ID = -1009999999999

    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "ð’ð­ð«ð¢ð§ð  ð’ðžð¬ð¬ð¢ð¨ð§ ðð¨ð­ ð…ð¢ð¥ð¥ðžð, ðð¥ðžðšð¬ðž ð…ð¢ð¥ð¥ ð€ ðð²ð«ð¨ð ð«ðšð¦ V2 ð’ðžð¬ð¬ð¢ð¨ð§ðŸ¤¬"
        )

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("IMMORTAL_MUSIC.plugins" + all_module)
    LOGGER("IMMORTAL_MUSIC.plugins").info("All features loaded.")
    await userbot.start()
    await NOBITA.start()
    await NOBITA.decorators()
    LOGGER("IMMORTAL_MUSIC").info("Immortal bot started.")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("IMMORTAL_MUSIC").info("Immortal bot stopped.")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())

