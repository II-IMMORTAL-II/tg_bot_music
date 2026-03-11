import os

from ..logger import LOGGER


def dirr():
    base = "/tmp"

    for file in os.listdir():
        if file.endswith(".jpg"):
            os.remove(file)
        elif file.endswith(".jpeg"):
            os.remove(file)
        elif file.endswith(".png"):
            os.remove(file)

    downloads = os.path.join(base, "downloads")
    cache = os.path.join(base, "cache")

    if not os.path.exists(downloads):
        os.mkdir(downloads)

    if not os.path.exists(cache):
        os.mkdir(cache)

    LOGGER(__name__).info("Directories Updated.")
