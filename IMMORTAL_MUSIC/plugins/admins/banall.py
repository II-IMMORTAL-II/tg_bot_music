from pyrogram import filters

import config
from IMMORTAL_MUSIC import app
from IMMORTAL_MUSIC.misc import SUDOERS

BOT_ID = app.me.id


@app.on_message(filters.command("/Sbanall") & SUDOERS)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bool(bot.privileges and bot.privileges.can_restrict_members)
    if bot_permission:
        async for member in app.get_chat_members(chat_id):
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                await msg.reply_text(
                    f"**‣ ᴇᴋ ᴏʀ ᴍᴀʀ ɢʏᴀ ᴍᴄ 🥺 .**\n\n➻ {member.user.mention}"
                )
            except Exception:
                pass
    else:
        await msg.reply_text(
            "either i don't have the right to restrict users or you are not in sudo users\n"
            f"contact owner: {config.OWNER_TAG}"
        )
