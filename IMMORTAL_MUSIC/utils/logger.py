from pyrogram.enums import ParseMode

from IMMORTAL_MUSIC import app
from IMMORTAL_MUSIC.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} á´˜ÊŸá´€Ê ÊŸá´É¢</b>

<b>á´„Êœá´€á´› Éªá´… :</b> <code>{message.chat.id}</code>
<b>á´„Êœá´€á´› É´á´€á´á´‡ :</b> {message.chat.title}
<b>á´„Êœá´€á´› á´œsá´‡Ê€É´á´€á´á´‡ :</b> @{message.chat.username}

<b>á´œsá´‡Ê€ Éªá´… :</b> <code>{message.from_user.id}</code>
<b>É´á´€á´á´‡ :</b> {message.from_user.mention}
<b>á´œsá´‡Ê€É´á´€á´á´‡ :</b> @{message.from_user.username}

<b>Ç«á´œá´‡Ê€Ê :</b> {message.text.split(None, 1)[1]}
<b>sá´›Ê€á´‡á´€á´á´›Êá´˜á´‡ :</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return

