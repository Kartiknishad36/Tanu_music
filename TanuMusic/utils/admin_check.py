from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus


async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return False
    if message.from_user.id in [
        777000,  # Telegram
        1087968824,  # Group Anonymous
    ]:
        return True
    check = await message.chat.get_member(message.from_user.id)
    if check.status not in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
    ]:
        return False
    if not check.privileges or not check.privileges.can_manage_video_chats:
        return False
    return True
