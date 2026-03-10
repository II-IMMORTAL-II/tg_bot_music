from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from IMMORTAL_MUSIC import app


def _htext(_, key, fallback):
    return _.get(key, fallback)


def help_pannel(_, page: Union[int, None] = 1):
    page = 1 if page not in (1, 2) else page

    page_1 = [
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_1", "Admin"),
                callback_data="help_callback hb1",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_2", "Auth"),
                callback_data="help_callback hb2",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_3", "Gcast"),
                callback_data="help_callback hb3",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_4", "Blacklist Chat"),
                callback_data="help_callback hb4",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_5", "Blacklist Users"),
                callback_data="help_callback hb5",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_6", "Channel Play"),
                callback_data="help_callback hb6",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_7", "Gban"),
                callback_data="help_callback hb7",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_8", "Loop"),
                callback_data="help_callback hb8",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_9", "Logger"),
                callback_data="help_callback hb9",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_10", "Ping"),
                callback_data="help_callback hb10",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_11", "Play"),
                callback_data="help_callback hb11",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_12", "Shuffle"),
                callback_data="help_callback hb12",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_13", "Seek"),
                callback_data="help_callback hb13",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_14", "Song"),
                callback_data="help_callback hb14",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_15", "Speed"),
                callback_data="help_callback hb15",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "ALL_COMMANDS", "All Commands"),
                callback_data="help_all 1",
            ),
            InlineKeyboardButton(
                text=_htext(_, "NEXT_PAGE", ">"),
                callback_data="help_page 2",
            ),
            InlineKeyboardButton(
                text=_htext(_, "CLOSE_BUTTON", "Close"),
                callback_data="close",
            ),
        ],
    ]

    page_2 = [
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_16", "GPT"),
                callback_data="help_callback hb16",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_17", "Sticker"),
                callback_data="help_callback hb17",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_18", "Tag All"),
                callback_data="help_callback hb18",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_19", "Info"),
                callback_data="help_callback hb19",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_20", "Group"),
                callback_data="help_callback hb20",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_21", "Extra"),
                callback_data="help_callback hb21",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "H_B_22", "Image"),
                callback_data="help_callback hb22",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_23", "Action"),
                callback_data="help_callback hb23",
            ),
            InlineKeyboardButton(
                text=_htext(_, "H_B_24", "Search"),
                callback_data="help_callback hb24",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_htext(_, "ALL_COMMANDS", "All Commands"),
                callback_data="help_all 1",
            ),
            InlineKeyboardButton(
                text=_htext(_, "BACK_PAGE", "<"),
                callback_data="help_page 1",
            ),
            InlineKeyboardButton(
                text=_htext(_, "BACK_BUTTON", "Back"),
                callback_data="settings_back_helper",
            ),
            InlineKeyboardButton(
                text=_htext(_, "CLOSE_BUTTON", "Close"),
                callback_data="close",
            ),
        ],
    ]

    return InlineKeyboardMarkup(page_1 if page == 1 else page_2)


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
