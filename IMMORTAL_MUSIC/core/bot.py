from pyrogram import Client, errors
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
import sqlite3

import config

from ..logger import LOGGER


class NOBITA(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="IMMORTAL_MUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        try:
            await super().start()
        except FloodWait as ex:
            LOGGER(__name__).error(
                f"Telegram rate limit hit (FLOOD_WAIT). Retry after {ex.value} seconds."
            )
            raise SystemExit(1)
        except sqlite3.OperationalError as ex:
            if "database is locked" in str(ex).lower():
                LOGGER(__name__).error(
                    "Pyrogram session DB is locked. Stop other running bot/python process and retry."
                )
                raise SystemExit(1)
            raise
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>Â» {self.mention} Ê™á´á´› sá´›á´€Ê€á´›á´‡á´… :</b><u>\n\nÉªá´… : <code>{self.id}</code>\nÉ´á´€á´á´‡ : {self.name}\ná´œsá´‡Ê€É´á´€á´á´‡ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )

        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )

        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
        except Exception as ex:
            LOGGER(__name__).warning(
                f"Skipping log group admin check due to invalid LOGGER_ID/access. Reason: {type(ex).__name__}."
            )

        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

