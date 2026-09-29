import sys
import traceback
from functools import wraps

from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from TanuMusic import LOGGER, app


def split_limits(text):
    if len(text) < 2048:
        return [text]
    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    result.append(small_msg)
    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(exc_type, exc_obj, exc_tb)
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    message.from_user.mention if message.from_user else 0,
                    message.chat.id if message.chat else 0,
                    message.text or message.caption or "",
                    "".join(errors),
                )
            )
            for x in error_feedback:
                try:
                    await app.send_message(config_logger(), x)
                except Exception:
                    LOGGER(__name__).error(x)
            raise err

    return capture


def config_logger():
    import config

    return config.LOGGER_ID
