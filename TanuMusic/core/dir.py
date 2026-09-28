# ===============================================================================
# dir.py - Directory Management
# ===============================================================================
from pathlib import Path
from TanuMusic import logger

def ensure_dirs():
    for dir in ["cache", "downloads"]:
        Path(dir).mkdir(parents=True, exist_ok=True)
    logger.info("Cache directories updated.")
