import os
import sys
import asyncio
import importlib
import traceback
# Python 3.10+ removed the implicit event loop creation in asyncio.get_event_loop().
# Pyrogram's sync.py calls get_event_loop() at import time, so we must create
# and set a new event loop BEFORE importing anything from pyrogram.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import idle
from pyrogram import utils as pyrogram_utils

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from IMMORTAL_MUSIC import LOGGER, app, userbot
from IMMORTAL_MUSIC.core.call import IMMORTAL
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
            "String session not filled. Please fill at least one Pyrogram V2 string session."
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
    loaded_modules = 0
    failed_modules = 0
    for all_module in ALL_MODULES:
        module_name = "IMMORTAL_MUSIC.plugins" + all_module
        try:
            importlib.import_module(module_name)
            loaded_modules += 1
        except Exception as exc:
            failed_modules += 1
            LOGGER("IMMORTAL_MUSIC.plugins").warning(
                f"Skipping plugin {module_name}: {type(exc).__name__}: {exc}"
            )
            LOGGER("IMMORTAL_MUSIC.plugins").debug(traceback.format_exc())
    LOGGER("IMMORTAL_MUSIC.plugins").info(
        f"Plugin load complete. loaded={loaded_modules}, failed={failed_modules}"
    )
    await userbot.start()
    await IMMORTAL.start()
    await IMMORTAL.decorators()
    LOGGER("IMMORTAL_MUSIC").info("Immortal bot started.")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("IMMORTAL_MUSIC").info("Immortal bot stopped.")


if __name__ == "__main__":
    loop.run_until_complete(init())


