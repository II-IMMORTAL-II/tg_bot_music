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
                    photo="https://files.catbox.moe/tcz7s6.jpg", caption=f"According to my database, you have not joined [Support]({link}) yet. Join [Support]({link}) and then start me again.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Join Support", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Please promote me as an admin in the must_join chat: {MUST_JOIN} !")

