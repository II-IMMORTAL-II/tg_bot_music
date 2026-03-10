import io
import logging
import os
import sys

from IMMORTAL_MUSIC.text_normalizer import normalize_text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

LOG_STREAM = sys.stdout
if hasattr(sys.stdout, "buffer"):
    LOG_STREAM = io.TextIOWrapper(
        sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
    )

handlers = [logging.StreamHandler(LOG_STREAM)]
try:
    file_path = os.environ.get("LOG_FILE", "log.txt")
    handlers.insert(0, logging.FileHandler(file_path, encoding="utf-8"))
except OSError:
    # Running on read-only filesystem; stream-only logging keeps the app alive.
    pass

logging.basicConfig(
    force=True,
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=handlers,
)


class _AsyncioSocketSendFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Harmless noisy warning on flaky sockets; keep other asyncio logs visible.
        message = record.getMessage()
        if record.name == "asyncio" and "socket.send() raised exception." in message:
            return False
        return True


class _LogTextNormalizeFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = normalize_text(record.msg)
        if isinstance(record.args, tuple):
            record.args = tuple(normalize_text(a) for a in record.args)
        elif isinstance(record.args, dict):
            record.args = {k: normalize_text(v) for k, v in record.args.items()}
        return True


logging.getLogger().addFilter(_LogTextNormalizeFilter())
logging.getLogger("asyncio").addFilter(_AsyncioSocketSendFilter())
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
