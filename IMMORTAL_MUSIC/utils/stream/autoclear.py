import os
import time

from config import autoclean

_LAST_SWEEP = 0
SWEEP_INTERVAL = 300
FILE_TTL = 900


def _sweep_temp_dirs():
    global _LAST_SWEEP
    now = time.time()
    if now - _LAST_SWEEP < SWEEP_INTERVAL:
        return
    _LAST_SWEEP = now

    tracked_files = set()
    for path in autoclean:
        if isinstance(path, str):
            tracked_files.add(os.path.abspath(path))

    for temp_dir in ("cache", "downloads"):
        if not os.path.isdir(temp_dir):
            continue

        for root, _, files in os.walk(temp_dir):
            for name in files:
                fpath = os.path.abspath(os.path.join(root, name))
                if fpath in tracked_files:
                    continue
                try:
                    if now - os.path.getmtime(fpath) < FILE_TTL:
                        continue
                    os.remove(fpath)
                except:
                    pass


async def auto_clean(popped):
    try:
        rem = popped["file"]
        autoclean.remove(rem)
        count = autoclean.count(rem)
        if count == 0:
            # Only remove local downloaded files, skip virtual queue ids like vid_/live_/index_.
            if (
                "vid_" not in rem
                and "live_" not in rem
                and "index_" not in rem
                and os.path.isfile(rem)
            ):
                try:
                    os.remove(rem)
                except:
                    pass
    except:
        pass
    try:
        _sweep_temp_dirs()
    except:
        pass
