from TanuMusic.misc import db


async def put(
    chat_id,
    original_chat_id,
    file,
    title,
    duration,
    user,
    vidid,
    stream="audio",
    forceplay=False,
):
    if stream == "audio":
        try:
            from TanuMusic.utils.formatters import seconds_to_min
            from TanuMusic import YouTube

            n, file_path = await YouTube.download(file, mystic=None, video=False)
            dur = 0
            put = {
                "title": title,
                "dur": duration,
                "streamtype": stream,
                "by": user,
                "chat_id": original_chat_id,
                "file": file_path if n else file,
                "vidid": vidid,
                "seconds": dur,
                "played": 0,
            }
        except Exception:
            put = {
                "title": title,
                "dur": duration,
                "streamtype": stream,
                "by": user,
                "chat_id": original_chat_id,
                "file": file,
                "vidid": vidid,
                "seconds": 0,
                "played": 0,
            }
    else:
        put = {
            "title": title,
            "dur": duration,
            "streamtype": stream,
            "by": user,
            "chat_id": original_chat_id,
            "file": file,
            "vidid": vidid,
            "seconds": 0,
            "played": 0,
        }
    if forceplay:
        check = db.get(chat_id)
        if check:
            check.insert(0, put)
        else:
            db[chat_id] = []
            db[chat_id].append(put)
    else:
        if chat_id not in db:
            db[chat_id] = []
        db[chat_id].append(put)
