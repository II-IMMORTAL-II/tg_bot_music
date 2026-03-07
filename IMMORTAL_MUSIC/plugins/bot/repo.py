from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from IMMORTAL_MUSIC import app
import config
from IMMORTAL_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """
âœ° ð—ªá´‡ÊŸá´„á´á´á´‡ á´›á´ ð—¥á´‡á´˜á´s âœ°
 
âœ° ð—¥á´‡á´˜á´ á´›á´ ð—¡ÊœÉª ð— ÉªÊŸá´‡É¢á´€ ð—¬Êœá´€
 
âœ° ð—£á´€ÊœÊŸá´‡ ð—£á´€á´˜á´€ ð—•á´ÊŸ ð—¥á´‡á´˜á´ ð—¢á´¡É´á´‡Ê€ á´‹á´ 

âœ° || {owner} ||
 
âœ° ð—¥á´œÉ´ 24x7 ð—Ÿá´€É¢ ð—™Ê€á´‡á´‡ ð—ªÉªá´›Êœá´á´œá´› ð—¦á´›á´á´˜
 
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    owner_tag = config.OWNER_TAG
    buttons = [
        [ 
          InlineKeyboardButton("ð—”á´…á´… á´á´‡ ð— á´€Ê™Ê", url=f"https://t.me/{config.BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("ð—›á´‡ÊŸá´˜", url=config.SUPPORT_CHAT),
          InlineKeyboardButton("ðš´ ðŽ ð ðš° ð“ ðš²", url=f"https://t.me/{config.OWNER_USERNAME}"),
          ],
               [
                InlineKeyboardButton("Ë¹sá´œá´˜á´˜á´Ê€á´› á´„Êœá´€á´›Ë¼", url=config.SUPPORT_CHAT),
],
[
InlineKeyboardButton("ð—–Êœá´€É´É´á´‡ÊŸ", url=config.SUPPORT_CHANNEL),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo=config.START_IMG_URL,
        caption=start_txt.format(owner=owner_tag),
        reply_markup=reply_markup
    )
