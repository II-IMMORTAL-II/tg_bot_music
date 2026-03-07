import math

from pyrogram.types import InlineKeyboardButton

from IMMORTAL_MUSIC.utils.formatters import time_to_seconds
import config


def _progress_bar(played, total, width=10):
    if total <= 0:
        return "[----------]"
    ratio = min(max(played / total, 0), 1)
    pos = min(width - 1, math.floor(ratio * width))
    chars = ["-"] * width
    chars[pos] = ">"
    return "[" + "".join(chars) + "]"


def _admin_controls(chat_id):
    return [
        InlineKeyboardButton(text="Resume", callback_data=f"ADMIN Resume|{chat_id}"),
        InlineKeyboardButton(text="Pause", callback_data=f"ADMIN Pause|{chat_id}"),
        InlineKeyboardButton(text="Replay", callback_data=f"ADMIN Replay|{chat_id}"),
        InlineKeyboardButton(text="Skip", callback_data=f"ADMIN Skip|{chat_id}"),
        InlineKeyboardButton(text="Stop", callback_data=f"ADMIN Stop|{chat_id}"),
    ]


def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]


def stream_markup_timer(_, videoid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    bar = _progress_bar(played_sec, duration_sec)

    return [
        _admin_controls(chat_id),
        [InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")],
        [
            InlineKeyboardButton(
                text="Owner", url=f"https://t.me/{config.OWNER_USERNAME}"
            ),
            InlineKeyboardButton(text="Support", url=config.SUPPORT_CHAT),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]


def stream_markup(_, videoid, chat_id):
    return [
        _admin_controls(chat_id),
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"IMMORTALPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"IMMORTALPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    return [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="<",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text=">",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]


def queue_markup(_, videoid, chat_id):
    return [
        _admin_controls(chat_id),
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]


def telegram_markup(_, chat_id):
    return [
        _admin_controls(chat_id),
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]


def telegram_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    bar = _progress_bar(played_sec, duration_sec)

    return [
        [InlineKeyboardButton(text=f"{dur} {bar} {played}", callback_data="GetTimer")],
        _admin_controls(chat_id),
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]
