from IMMORTAL_MUSIC.misc import SUDOERS
from IMMORTAL_MUSIC.utils.database import get_lang, is_maintenance
from strings import get_string


def language(mystic):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} Éªs á´œÉ´á´…á´‡Ê€ á´á´€ÉªÉ´á´›á´‡É´á´€É´á´„á´‡, á´ ÉªsÉªá´› <a href={SUPPORT_CHAT}>sá´œá´˜á´˜á´Ê€á´› á´„Êœá´€á´›</a> Ò“á´Ê€ á´‹É´á´á´¡ÉªÉ´É¢ á´›Êœá´‡ Ê€á´‡á´€sá´É´.",
                    disable_web_page_preview=True,
                )
        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} Éªs á´œÉ´á´…á´‡Ê€ á´á´€ÉªÉ´á´›á´‡É´á´€É´á´„á´‡, á´ ÉªsÉªá´› sá´œá´˜á´˜á´Ê€á´› á´„Êœá´€á´› Ò“á´Ê€ á´‹É´á´á´¡ÉªÉ´É¢ á´›Êœá´‡ Ê€á´‡á´€sá´É´.",
                    show_alert=True,
                )
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("en")
        return await mystic(_, message, language)

    return wrapper

