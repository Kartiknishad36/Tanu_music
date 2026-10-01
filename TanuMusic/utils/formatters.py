import os
import re
import time
from typing import Union

formats = [
    "webm", "mkv", "flv", "vob", "ogv", "ogg", "rrc", "gifv", "mng",
    "mov", "avi", "qt", "wmv", "yuv", "rm", "asf", "amv", "mp4",
    "m4p", "m4v", "mpg", "mp2", "mpeg", "mpe", "mpv", "svi", "3gp",
    "3g2", "mxf", "roq", "nsv", "flv", "f4v", "f4p", "f4a", "f4b",
]


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


def convert_bytes(size: float) -> str:
    if not size:
        return ""
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            (seconds // 3600) % 24,
            (seconds % 3600) // 60,
            (seconds % 3600) % 60,
        )
        if d > 0:
            return f"{d:02d}:{h:02d}:{m:02d}:{s:02d}"
        elif h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        elif m > 0:
            return f"{m:02d}:{s:02d}"
        else:
            return f"00:{s:02d}"
    return "Unknown"


def speed_converter(seconds, speed):
    if not speed or float(speed) == 1.0:
        return seconds
    return int(float(seconds) / float(speed))


async def check_duration(file_path):
    try:
        import asyncio

        out = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await out.communicate()
        return float(stdout.decode().strip() or 0)
    except Exception:
        return 0


def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = str(user_id)
    return "".join(alphabet[int(i)] for i in user_id)


def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        user_id += str(alphabet.index(i))
    return int(user_id)
