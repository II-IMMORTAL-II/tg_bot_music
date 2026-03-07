import inspect
import re
from functools import wraps

SUSPECT_TOKENS = ("Ã", "Â", "â", "ð", "á", "É", "Ê", "Ò", "à¹", "�")
COMMON_FIXES = {
    "âœ…": "✅",
    "âŒ": "❌",
    "â": "❍",
    "âœ¦": "•",
    "â€”": "-",
    "â€“": "-",
    "â€˜": "'",
    "â€™": "'",
    "â€œ": '"',
    "â€": '"',
    "Â»": "»",
    "Â«": "«",
    "Â": "",
}
SMALLCAPS_MAP = str.maketrans(
    {
        "ᴀ": "a",
        "ʙ": "b",
        "ᴄ": "c",
        "ᴅ": "d",
        "ᴇ": "e",
        "ꜰ": "f",
        "ɢ": "g",
        "ʜ": "h",
        "ɪ": "i",
        "ᴊ": "j",
        "ᴋ": "k",
        "ʟ": "l",
        "ᴍ": "m",
        "ɴ": "n",
        "ᴏ": "o",
        "ᴘ": "p",
        "ǫ": "q",
        "ʀ": "r",
        "ᴛ": "t",
        "ᴜ": "u",
        "ᴠ": "v",
        "ᴡ": "w",
        "ʏ": "y",
        "ᴢ": "z",
    }
)
SPACE_RE = re.compile(r"[ \t]{2,}")
NEWLINES_RE = re.compile(r"\n{3,}")

CP1252_EXTRA_REVERSE = {}
for _byte in range(0x80, 0xA0):
    try:
        _char = bytes([_byte]).decode("cp1252")
    except Exception:
        continue
    CP1252_EXTRA_REVERSE[_char] = _byte


def _has_suspect_tokens(text):
    return any(token in text for token in SUSPECT_TOKENS)


def _score_candidate(text):
    score = 0
    for token in SUSPECT_TOKENS:
        score += text.count(token) * 3
    score += text.count("�") * 5
    return score


def _to_pseudo_bytes(text):
    raw = bytearray()
    for char in text:
        code = ord(char)
        if code <= 0xFF:
            raw.append(code)
            continue
        mapped = CP1252_EXTRA_REVERSE.get(char)
        if mapped is None:
            return None
        raw.append(mapped)
    return bytes(raw)


def _decode_candidate(text):
    candidates = [text]
    for source_encoding in ("latin1", "cp1252"):
        try:
            candidates.append(text.encode(source_encoding).decode("utf-8"))
        except Exception:
            pass

    pseudo_bytes = _to_pseudo_bytes(text)
    if pseudo_bytes:
        try:
            candidates.append(pseudo_bytes.decode("utf-8"))
        except Exception:
            pass

    return candidates


def normalize_text(value):
    if not isinstance(value, str):
        return value

    out = value
    for _ in range(3):
        if not _has_suspect_tokens(out):
            break
        candidates = _decode_candidate(out)
        best = min(candidates, key=_score_candidate)
        if best == out:
            break
        out = best

    for source, target in COMMON_FIXES.items():
        out = out.replace(source, target)

    out = out.translate(SMALLCAPS_MAP)
    out = SPACE_RE.sub(" ", out)
    out = NEWLINES_RE.sub("\n\n", out)
    return out.strip()


def normalize_reply_markup(markup):
    if not hasattr(markup, "inline_keyboard"):
        return markup
    try:
        for row in markup.inline_keyboard:
            for button in row:
                if hasattr(button, "text") and isinstance(button.text, str):
                    button.text = normalize_text(button.text)
    except Exception:
        return markup
    return markup


def _patch_async_method(cls, method_name, text_params):
    original = getattr(cls, method_name, None)
    if not original or getattr(original, "_text_normalized", False):
        return

    signature = inspect.signature(original)

    @wraps(original)
    async def wrapper(*args, **kwargs):
        bound = signature.bind_partial(*args, **kwargs)
        for param in text_params:
            if param in bound.arguments:
                bound.arguments[param] = normalize_text(bound.arguments[param])
        if "reply_markup" in bound.arguments:
            bound.arguments["reply_markup"] = normalize_reply_markup(
                bound.arguments["reply_markup"]
            )
        return await original(*bound.args, **bound.kwargs)

    wrapper._text_normalized = True
    setattr(cls, method_name, wrapper)


def patch_text_pipeline():
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media.message import Message

    client_methods = {
        "send_message": ("text",),
        "send_photo": ("caption",),
        "send_video": ("caption",),
        "send_document": ("caption",),
        "send_audio": ("caption",),
        "send_voice": ("caption",),
        "send_animation": ("caption",),
        "send_media_group": ("caption",),
        "edit_message_text": ("text",),
        "edit_message_caption": ("caption",),
        "answer_callback_query": ("text",),
    }
    for method_name, text_params in client_methods.items():
        _patch_async_method(Client, method_name, text_params)

    message_methods = {
        "reply": ("text",),
        "reply_text": ("text",),
        "reply_photo": ("caption",),
        "reply_video": ("caption",),
        "reply_audio": ("caption",),
        "reply_document": ("caption",),
        "reply_animation": ("caption",),
        "edit": ("text",),
        "edit_text": ("text",),
        "edit_caption": ("caption",),
    }
    for method_name, text_params in message_methods.items():
        _patch_async_method(Message, method_name, text_params)
