from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from IMMORTAL_MUSIC import app
import config

#--------------------------
MUST_JOIN = config.SUPPORT_CHANNEL_USERNAME or config.SUPPORT_CHANNEL
#------------------------
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if config.SUPPORT_CHANNEL_USERNAME:
                link = f"https://t.me/{config.SUPPORT_CHANNEL_USERNAME}"
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply_photo(
                    photo="https://files.catbox.moe/tcz7s6.jpg", caption=f"à¹ á´€á´„á´„á´Ê€á´…ÉªÉ´É¢ á´›á´ á´Ê á´…á´€á´›á´€Ê™á´€sá´‡ Êá´á´œ'á´ á´‡ É´á´á´› á´Šá´ÉªÉ´á´‡á´… [à¹sá´œá´˜á´˜á´Ê€á´›à¹]({link}) Êá´‡á´›, ÉªÒ“ Êá´á´œ á´¡á´€É´á´› á´›á´ á´œsá´‡ á´á´‡ á´›Êœá´‡É´ á´Šá´ÉªÉ´ [à¹sá´œá´˜á´˜á´Ê€á´›à¹]({link}) á´€É´á´… sá´›á´€Ê€á´› á´á´‡ á´€É¢á´€ÉªÉ´ ! ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("â€¢ á´Šá´ÉªÉ´ â€¢", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"à¹ á´˜Ê€á´á´á´á´›á´‡ á´á´‡ á´€s á´€É´ á´€á´…á´ÉªÉ´ ÉªÉ´ á´›Êœá´‡ á´á´œsá´›_á´Šá´ÉªÉ´ á´„Êœá´€á´› à¹: {MUST_JOIN} !")

