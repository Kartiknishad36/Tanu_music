import os

try:
    from config import autoclean
except ImportError:
    autoclean = []

if not isinstance(autoclean, list):
    autoclean = []


async def auto_clean(popped):
    try:
        if not popped:
            return
        rem = popped.get("file") if isinstance(popped, dict) else None
        if not rem:
            return
        try:
            while rem in autoclean:
                autoclean.remove(rem)
        except ValueError:
            pass
        count = autoclean.count(rem) if isinstance(autoclean, list) else 0
        if count == 0:
            if not ("vid_" in str(rem) or "live_" in str(rem) or "index_" in str(rem)):
                try:
                    if os.path.isfile(rem):
                        os.remove(rem)
                except Exception:
                    pass
    except Exception:
        pass
