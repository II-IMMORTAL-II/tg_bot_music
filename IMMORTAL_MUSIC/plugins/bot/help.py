from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from IMMORTAL_MUSIC import app
from IMMORTAL_MUSIC.utils import help_pannel
from IMMORTAL_MUSIC.utils.database import get_lang
from IMMORTAL_MUSIC.utils.decorators.language import LanguageStart, languageCB
from IMMORTAL_MUSIC.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers

EXTRA_HELP = {
    "hb16": "**GPT Commands**\n\n`/ask <query>` - Ask AI and get a reply.",
    "hb17": "**Sticker Commands**\n\n`/kang`\n`/stickerid`\n`/packkang`\n`/mmf <name>`",
    "hb18": "**Tag-All Commands**\n\n`/tagall` ` /tagoff`\n`/hitag` ` /histop`\n`/gmtag` ` /gmstop`\n`/gntag` ` /gnstop`\n`/shayari` ` /shstop`\n`/utag` ` /cancel`",
    "hb19": "**Info Commands**\n\n`/id`\n`/info`\n`/stats`\n`/ping`",
    "hb20": "**Group Commands**\n\n`/pin` ` /unpin` ` /pinned`\n`/settitle` ` /setdescription`\n`/setphoto` ` /removephoto`\n`/staff` ` /bots`",
    "hb21": "**Extra Commands**\n\n`/math`\n`/tgm`\n`/tr`\n`/google`\n`/gemini`\n`/afk`",
    "hb22": "**Image Commands**\n\n`/image <query>`\n`/imgs <query>`\n`/reel <instagram_link>`",
    "hb23": "**Action Commands**\n\n`/ban` ` /unban`\n`/mute` ` /unmute`\n`/kick`\n`/tmute` ` /tban`",
    "hb24": "**Search Commands**\n\n`/google <query>`\n`/app <query>`\n`/stack <query>`\n`/image <query>`",
}


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except Exception:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, 1)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except Exception:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_, 1)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("^help_page") & ~BANNED_USERS)
@languageCB
async def help_page_cb(client, CallbackQuery, _):
    page = 1
    parts = CallbackQuery.data.split(maxsplit=1)
    if len(parts) > 1 and parts[1] == "2":
        page = 2
    await CallbackQuery.edit_message_reply_markup(reply_markup=help_pannel(_, page))


@app.on_callback_query(filters.regex("^help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)

    default_help = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
    }

    text = default_help.get(cb) or EXTRA_HELP.get(cb)
    if not text:
        await CallbackQuery.answer("Help section not found.", show_alert=True)
        return

    await CallbackQuery.edit_message_text(text, reply_markup=keyboard)
