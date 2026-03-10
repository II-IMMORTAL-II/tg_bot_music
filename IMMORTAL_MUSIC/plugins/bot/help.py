from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

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


def _extract_filter_commands(flt) -> set:
    commands = set()
    if not flt:
        return commands

    direct = getattr(flt, "commands", None)
    if direct:
        commands.update(direct)

    for attr in ("base", "other"):
        child = getattr(flt, attr, None)
        if child is not None:
            commands.update(_extract_filter_commands(child))

    return commands


def _normalize_command_name(command: str) -> str:
    name = str(command).strip().lower().lstrip("/")
    if not name or any(ch.isspace() for ch in name):
        return ""

    username = getattr(app, "username", None)
    if username:
        suffix = f"@{username.lower()}"
        if name.endswith(suffix):
            name = name[: -len(suffix)]

    return name


def _all_registered_commands() -> list:
    commands = set()
    dispatcher = getattr(app, "dispatcher", None)
    groups = getattr(dispatcher, "groups", {}) if dispatcher else {}

    for handlers in groups.values():
        for handler in handlers:
            commands.update(_extract_filter_commands(getattr(handler, "filters", None)))

    normalized = set()
    for command in commands:
        name = _normalize_command_name(command)
        if name:
            normalized.add(name)

    return sorted(normalized)


def _all_commands_page(page: int):
    page_size = 45
    commands = _all_registered_commands()
    if not commands:
        return "No commands found.", 1, 1

    total_pages = (len(commands) + page_size - 1) // page_size
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    chunk = commands[start : start + page_size]

    text = (
        f"All Commands ({len(commands)})\n"
        f"Page {page}/{total_pages}\n\n"
        + "\n".join(f"• /{cmd}" for cmd in chunk)
    )
    return text, page, total_pages


def _all_commands_markup(_, page: int, total_pages: int):
    rows = []
    nav = []
    if page > 1:
        nav.append(
            InlineKeyboardButton(
                text=_.get("BACK_PAGE", "<"), callback_data=f"help_all {page - 1}"
            )
        )
    if page < total_pages:
        nav.append(
            InlineKeyboardButton(
                text=_.get("NEXT_PAGE", ">"), callback_data=f"help_all {page + 1}"
            )
        )
    if nav:
        rows.append(nav)

    rows.append(
        [
            InlineKeyboardButton(
                text=_.get("BACK_BUTTON", "Back"), callback_data="settings_back_helper"
            ),
            InlineKeyboardButton(text=_.get("CLOSE_BUTTON", "Close"), callback_data="close"),
        ]
    )
    return InlineKeyboardMarkup(rows)


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


@app.on_callback_query(filters.regex("^help_all") & ~BANNED_USERS)
@languageCB
async def help_all_cb(client, CallbackQuery, _):
    page = 1
    parts = CallbackQuery.data.split(maxsplit=1)
    if len(parts) > 1 and parts[1].isdigit():
        page = int(parts[1])

    text, page, total_pages = _all_commands_page(page)
    await CallbackQuery.edit_message_text(
        text, reply_markup=_all_commands_markup(_, page, total_pages)
    )
