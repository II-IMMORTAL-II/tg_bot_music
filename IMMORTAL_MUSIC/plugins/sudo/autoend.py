from pyrogram import filters
from pyrogram.types import Message

from IMMORTAL_MUSIC import app
from IMMORTAL_MUSIC.misc import SUDOERS
from IMMORTAL_MUSIC.utils.database import autoend_off, autoend_on


@app.on_message(filters.command("autoend") & SUDOERS)
async def auto_end_stream(_, message: Message):
    usage = "<b>á´‡xá´€á´á´˜ÊŸá´‡ :</b>\n\n/autoend [á´‡É´á´€Ê™ÊŸá´‡ | á´…Éªsá´€Ê™ÊŸá´‡]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Â» á´€á´œá´›á´ á´‡É´á´… sá´›Ê€á´‡á´€á´ á´‡É´á´€Ê™ÊŸá´‡á´….\n\ná´€ssÉªsá´›á´€É´á´› á´¡ÉªÊŸÊŸ á´€á´œá´›á´á´á´€á´›Éªá´„á´€ÊŸÊŸÊ ÊŸá´‡á´€á´ á´‡ á´›Êœá´‡ á´ Éªá´…á´‡á´á´„Êœá´€á´› á´€Ò“á´›á´‡Ê€ Ò“á´‡á´¡ á´ÉªÉ´s á´¡Êœá´‡É´ É´á´ á´É´á´‡ Éªs ÊŸÉªsá´›á´‡É´ÉªÉ´É¢."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Â» á´€á´œá´›á´ á´‡É´á´… sá´›Ê€á´‡á´€á´ á´…Éªsá´€Ê™ÊŸá´‡á´….")
    else:
        await message.reply_text(usage)

