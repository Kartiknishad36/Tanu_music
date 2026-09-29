import os
from ..logging import LOGGER


def dirr():
    for file in os.listdir():
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            try:
                os.remove(file)
            except Exception:
                pass
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("cache"):
        os.makedirs("cache")
    LOGGER(__name__).info("Directories Updated!")
