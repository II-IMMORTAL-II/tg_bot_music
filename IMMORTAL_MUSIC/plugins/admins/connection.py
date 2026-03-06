from pyrogram import filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ChatMembersFilter
from IMMORTAL_MUSIC import app
from IMMORTAL_MUSIC.utils.database import connect_to_chat
from IMMORTAL_MUSIC.utils.decorators import AdminActual
from config import BANNED_USERS


@app.on_message(filters.command("connect") & filters.group & ~BANNED_USERS)
async def auth(client, message: Message):
    admin_ids = [ member.user.id async for member in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)]
    if not message.from_user.id in admin_ids:
        return 
    user_id = message.from_user.id
    chat_id = message.chat.id
   # re = await connect_to_chat(message.from_user.id, message.chat.id)
    
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("á´„á´É´É´á´‡á´„á´› á´›á´ á´„Êœá´€á´› ", url=f"http://t.me/{app.username}?start=connect_{chat_id}")]])
    await message.reply_text("á´›á´€á´˜ á´›Êœá´‡ Ò“á´ÊŸÊŸá´á´¡ÉªÉ´É¢ Ê™á´œá´›á´›á´É´ á´›á´ á´„á´É´É´á´‡á´„á´› á´›á´ á´›ÊœÉªs á´„Êœá´€á´› ÉªÉ´ á´˜á´", reply_markup = markup)

