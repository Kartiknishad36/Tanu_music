"""
Ensure assistant user account is inside the group before PyTgCalls play.
Fixes: CHANNEL_INVALID / PeerIdInvalid when assistant never joined the chat.
"""
import logging
from pyrogram import errors
from pyrogram.enums import ChatMemberStatus, ChatMembersFilter

from TanuMusic import app, userbot

log = logging.getLogger(__name__)


async def ensure_assistant_in_chat(chat_id: int) -> tuple[bool, str]:
    """
    Make sure at least one assistant is a member of chat_id.
    Returns (ok, message).
    """
    if not userbot.clients:
        return False, "No assistant connected (STRING_SESSION missing)."

    ub = userbot.clients[0]
    aid = getattr(ub, "id", None) or (ub.me.id if ub.me else None)
    if not aid:
        return False, "Assistant ID unknown."

    # 1) Already in chat?
    try:
        member = await ub.get_chat_member(chat_id, aid)
        if member and member.status not in (
            ChatMemberStatus.LEFT,
            ChatMemberStatus.BANNED,
        ):
            return True, "already_member"
    except errors.UserNotParticipant:
        pass
    except errors.ChannelPrivate:
        pass
    except errors.ChannelInvalid:
        pass
    except Exception as e:
        log.debug(f"get_chat_member assistant: {e}")

    # Also check from bot side
    try:
        member = await app.get_chat_member(chat_id, aid)
        if member and member.status not in (
            ChatMemberStatus.LEFT,
            ChatMemberStatus.BANNED,
        ):
            # Bot sees them but assistant client may lack peer — force get_chat
            try:
                await ub.get_chat(chat_id)
            except Exception:
                pass
            return True, "already_member_bot"
    except Exception:
        pass

    # 2) Bot invites assistant (needs "Invite Users" permission)
    try:
        await app.add_chat_members(chat_id, aid)
        log.info(f"Invited assistant {aid} to {chat_id}")
        try:
            await ub.get_chat(chat_id)
        except Exception:
            pass
        return True, "invited"
    except errors.UserAlreadyParticipant:
        try:
            await ub.get_chat(chat_id)
        except Exception:
            pass
        return True, "already_member"
    except errors.ChatAdminRequired:
        log.warning(f"Bot needs Invite Users right in {chat_id}")
    except errors.UserPrivacyRestricted:
        log.warning(f"Assistant privacy blocks invite in {chat_id}")
    except Exception as e:
        log.warning(f"add_chat_members failed: {e}")

    # 3) Export invite link → assistant joins
    try:
        link = await app.export_chat_invite_link(chat_id)
    except Exception:
        try:
            from pyrogram.types import ChatPrivileges

            # try create link
            inv = await app.create_chat_invite_link(chat_id, member_limit=1)
            link = inv.invite_link
        except Exception as e:
            log.error(f"Cannot export invite for {chat_id}: {e}")
            return (
                False,
                "❌ Assistant group me nahi hai.\n"
                "• Bot ko <b>Invite Users</b> admin right do\n"
                "• Ya assistant account ko manually group me add karo",
            )

    try:
        await ub.join_chat(link)
        log.info(f"Assistant joined {chat_id} via invite link")
        return True, "joined_link"
    except errors.UserAlreadyParticipant:
        return True, "already_member"
    except errors.InviteRequestSent:
        return (
            False,
            "⏳ Join request bhej diya — admin ko approve karna hoga assistant ka request.",
        )
    except Exception as e:
        log.error(f"Assistant join_chat failed: {e}")
        return (
            False,
            f"❌ Assistant auto-join fail: <code>{e}</code>\n"
            "Assistant account ko manually is group me add karo.",
        )
