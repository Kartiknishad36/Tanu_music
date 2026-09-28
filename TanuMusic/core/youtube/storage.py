import os
import glob
from pathlib import Path
from typing import Optional
from TanuMusic import logger

class StorageManager:
    def __init__(self, min_valid_bytes: int = 4096):
        self.MIN_VALID_BYTES = min_valid_bytes

    def is_valid_file(self, path: str) -> bool:
        try:
            return os.path.isfile(path) and os.path.getsize(path) >= self.MIN_VALID_BYTES
        except OSError:
            return False

    def delete_stub(self, path: str) -> None:
        try:
            os.remove(path)
            logger.warning(f"Deleted invalid cached file: {path}")
        except OSError:
            pass

    def locate_download_file(self, video_id: str, video: bool = False) -> Optional[str]:
        pattern = f"downloads/{video_id}*"
        candidates = sorted([
            path for path in glob.glob(pattern)
            if not path.endswith((".part", ".ytdl", ".info.json", ".temp"))
        ])

        video_exts = {".mp4", ".mkv", ".mov"}
        audio_exts = {".m4a", ".webm", ".opus", ".mp3", ".ogg", ".wav", ".flac"}

        prefer = video_exts if video else audio_exts
        for path in candidates:
            if os.path.isdir(path):
                continue
            if Path(path).suffix.lower() in prefer:
                if self.is_valid_file(path):
                    return path
                self.delete_stub(path)

        for path in candidates:
            if os.path.isdir(path):
                continue
            if self.is_valid_file(path):
                return path
            self.delete_stub(path)
        return None
