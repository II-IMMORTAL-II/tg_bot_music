from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters, Client
from IMMORTAL_MUSIC import app
from config import OWNER_ID
from pyrogram.types import Message
from IMMORTAL_MUSIC.utils.IMMORTAL_ban import admin_filter
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton



# ------------------------------------------------------------------------------- #


@app.on_message(filters.command("pin") & admin_filter)
async def pin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.mention
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("**á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹s á´É´ÊŸÊ á´É´ É¢Ê€á´á´œá´˜s !**")
    elif not replied:
        await message.reply_text("**Ê€á´‡á´˜ÊŸÊ á´›á´ á´€ á´á´‡ssá´€É¢á´‡ á´›á´ á´˜ÉªÉ´ Éªá´› !**")
    else:
        user_stats = await app.get_chat_member(chat_id, user_id)
        if user_stats.privileges.can_pin_messages and message.reply_to_message:
            try:
                await message.reply_to_message.pin()
                await message.reply_text(f"**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ á´˜ÉªÉ´É´á´‡á´… á´á´‡ssá´€É¢á´‡!**\n\n**á´„Êœá´€á´›:** {chat_title}\n**á´€á´…á´ÉªÉ´:** {name}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" ðŸ“ á´ Éªá´‡á´¡s á´á´‡ssá´€É¢á´‡ ", url=replied.link)]]))
            except Exception as e:
                await message.reply_text(str(e))


@app.on_message(filters.command("pinned"))
async def pinned(_, message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("**É´á´ á´˜ÉªÉ´É´á´‡á´… á´á´‡ssá´€É¢á´‡ Ò“á´á´œÉ´á´…**")
    try:        
        await message.reply_text("Êœá´‡Ê€á´‡ Éªs á´›Êœá´‡ ÊŸá´€á´›á´‡sá´› á´˜ÉªÉ´É´á´‡á´… á´á´‡ssá´€É¢á´‡",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="ðŸ“ á´ Éªá´‡á´¡ á´á´‡ssá´€É¢á´‡",url=chat.pinned_message.link)]]))  
    except Exception as er:
        await message.reply_text(er)


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command("unpin") & admin_filter)
async def unpin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.mention
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("**á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹s á´É´ÊŸÊ á´É´ É¢Ê€á´á´œá´˜s !**")
    elif not replied:
        await message.reply_text("**Ê€á´‡á´˜ÊŸÊ á´›á´ á´€ á´á´‡ssá´€É¢á´‡ á´›á´ á´œÉ´á´˜ÉªÉ´ Éªá´› !**")
    else:
        user_stats = await app.get_chat_member(chat_id, user_id)
        if user_stats.privileges.can_pin_messages and message.reply_to_message:
            try:
                await message.reply_to_message.unpin()
                await message.reply_text(f"**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ á´œÉ´á´˜ÉªÉ´É´á´‡á´… á´á´‡ssá´€É¢á´‡!**\n\n**á´„Êœá´€á´›:** {chat_title}\n**á´€á´…á´ÉªÉ´:** {name}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" ðŸ“ á´ Éªá´‡á´¡s á´á´‡ssá´€É¢á´‡ ", url=replied.link)]]))
            except Exception as e:
                await message.reply_text(str(e))




# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("removephoto") & admin_filter)
async def deletechatphoto(_, message):
      
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("**á´˜Ê€á´á´„á´‡ssÉªÉ´É¢....**")
      admin_check = await app.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("**á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹ á´É´ É¢Ê€á´á´œá´˜s !**") 
      try:
         if admin_check.privileges.can_change_info:
             await app.delete_chat_photo(chat_id)
             await msg.edit("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ Ê€á´‡á´á´á´ á´‡á´… á´˜Ê€á´Ò“ÉªÊŸá´‡ á´˜Êœá´á´›á´ Ò“Ê€á´á´ É¢Ê€á´á´œá´˜ !\nÊ™Ê** {}".format(message.from_user.mention))    
      except:
          await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´sá´› É´á´‡á´‡á´… á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ Ê€á´‡á´á´á´ á´‡ É¢Ê€á´á´œá´˜ á´˜Êœá´á´›á´ !**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("setphoto")& admin_filter)
async def setchatphoto(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("á´˜Ê€á´á´„á´‡ssÉªÉ´É¢...")
      admin_check = await app.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹ á´É´ É¢Ê€á´á´œá´˜s !`") 
      elif not reply:
           await msg.edit("**Ê€á´‡á´˜ÊŸÊ á´›á´ á´€ á´˜Êœá´á´›á´ á´Ê€ á´…á´á´„á´œá´á´‡É´á´›.**")
      elif reply:
          try:
             if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ É´á´‡á´¡ á´˜Ê€á´Ò“ÉªÊŸá´‡ á´˜Êœá´á´›á´ ÉªÉ´sá´‡Ê€á´› !\nÊ™Ê** {}".format(message.from_user.mention))
             else:
                await msg.edit("**sá´á´á´‡á´›ÊœÉªÉ´É¢ á´¡Ê€á´É´É¢ Êœá´€á´˜á´˜á´‡É´á´‡á´… á´›Ê€Ê á´€É´á´á´›Êœá´‡Ê€ á´˜Êœá´á´›á´ !**")
     
          except:
              await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´sá´› É´á´‡á´‡á´… á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´˜Êœá´á´›á´ !**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("settitle")& admin_filter)
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("á´˜Ê€á´á´„á´‡ssÉªÉ´É¢...")
    if message.chat.type == enums.ChatType.PRIVATE:
          await msg.edit("**á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹ á´É´ É¢Ê€á´á´œá´˜s !**")
    elif reply:
          try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ É´á´‡á´¡ É¢Ê€á´á´œá´˜ É´á´€á´á´‡ ÉªÉ´sá´‡Ê€á´› !\nÊ™Ê** {}".format(message.from_user.mention))
          except AttributeError:
                await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´sá´› É´á´‡á´‡á´… á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´›Éªá´›ÊŸá´‡ !**")   
    elif len(message.command) >1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ É´á´‡á´¡ É¢Ê€á´á´œá´˜ É´á´€á´á´‡ ÉªÉ´sá´‡Ê€á´› !\nÊ™Ê** {}".format(message.from_user.mention))
        except AttributeError:
               await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´sá´› É´á´‡á´‡á´… á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´›Éªá´›ÊŸá´‡ !**")
          

    else:
       await msg.edit("**Êá´á´œ É´á´‡á´‡á´… Ê€á´‡á´˜ÊŸÊ á´›á´ á´›á´‡xá´› á´Ê€ É¢Éªá´ á´‡ sá´á´á´‡ á´›á´‡xá´› á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´›Éªá´›ÊŸá´‡ **")


# --------------------------------------------------------------------------------- #



@app.on_message(filters.command("setdiscription") & admin_filter)
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**á´˜Ê€á´á´„á´‡ssÉªÉ´É¢...**")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**á´›ÊœÉªs á´„á´á´á´á´€É´á´… á´¡á´Ê€á´‹s á´É´ É¢Ê€á´á´œá´˜s!**")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ É´á´‡á´¡ É¢Ê€á´á´œá´˜ á´…Éªsá´„Ê€Éªá´˜á´›Éªá´É´ ÉªÉ´sá´‡Ê€á´›!**\nÊ™Ê {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´œsá´› Êœá´€á´ á´‡ á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´…Éªsá´„Ê€Éªá´˜á´›Éªá´É´!**")   
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ É´á´‡á´¡ É¢Ê€á´á´œá´˜ á´…Éªsá´„Ê€Éªá´˜á´›Éªá´É´ ÉªÉ´sá´‡Ê€á´›!**\nÊ™Ê {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("**á´›Êœá´‡ á´œsá´‡Ê€ á´á´œsá´› Êœá´€á´ á´‡ á´„Êœá´€É´É¢á´‡ ÉªÉ´Ò“á´ á´€á´…á´ÉªÉ´ Ê€ÉªÉ¢Êœá´›s á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´…Éªsá´„Ê€Éªá´˜á´›Éªá´É´!**")
    else:
        await msg.edit("**Êá´á´œ É´á´‡á´‡á´… á´›á´ Ê€á´‡á´˜ÊŸÊ á´›á´ á´›á´‡xá´› á´Ê€ É¢Éªá´ á´‡ sá´á´á´‡ á´›á´‡xá´› á´›á´ á´„Êœá´€É´É¢á´‡ É¢Ê€á´á´œá´˜ á´…Éªsá´„Ê€Éªá´˜á´›á´É´!**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("lg")& filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    text = "**sá´œá´„á´„á´‡ssÒ“á´œÊŸÊŸÊ ÊœÉªÊ€á´ !!.**"
    await message.reply_text(text)
    await app.leave_chat(chat_id=chat_id, delete=True)


# --------------------------------------------------------------------------------- #




