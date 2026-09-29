import json
import subprocess


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
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
    power_labels = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + power_labels[n] + "B"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


def speed_converter(seconds, speed):
    if str(speed) == str("0.5"):
        seconds = seconds * 2
    if str(speed) == str("0.75"):
        seconds = seconds + ((50 * seconds) // 100)
    if str(speed) == str("1.5"):
        seconds = seconds - ((25 * seconds) // 100)
    if str(speed) == str("2.0"):
        seconds = seconds - ((50 * seconds) // 100)
    collect = seconds
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            convert = "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
            return convert, collect
        elif h > 0:
            convert = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            return convert, collect
        elif m > 0:
            convert = "{:02d}:{:02d}".format(m, s)
            return convert, collect
        elif s > 0:
            convert = "00:{:02d}".format(s)
            return convert, collect
    return "-"


def check_duration(file_path):
    command = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    _json = json.loads(out)
    if "format" in _json:
        if "duration" in _json["format"]:
            return float(_json["format"]["duration"])
    if "streams" in _json:
        for s in _json["streams"]:
            if "duration" in s:
                return float(s["duration"])
    return "Unknown"
