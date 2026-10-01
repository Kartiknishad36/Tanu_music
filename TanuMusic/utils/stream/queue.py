from TanuMusic.misc import db


async def put_queue(
    chat_id,
    original_chat_id,
    file,
    title,
    duration,
    user,
    vidid,
    user_id=0,
    stream="audio",
    forceplay=False,
):
    put = {
        "title": title,
        "dur": duration,
        "streamtype": stream,
        "by": user,
        "user_id": user_id,
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
            db[chat_id] = [put]
    else:
        if chat_id not in db:
            db[chat_id] = []
        db[chat_id].append(put)
    return put


async def put_queue_index(
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
    return await put_queue(
        chat_id,
        original_chat_id,
        file,
        title,
        duration,
        user,
        vidid,
        0,
        stream,
        forceplay,
    )


# backward alias
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
    return await put_queue(
        chat_id,
        original_chat_id,
        file,
        title,
        duration,
        user,
        vidid,
        0,
        stream,
        forceplay,
    )
