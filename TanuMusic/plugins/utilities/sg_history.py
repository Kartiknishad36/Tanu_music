"""
/sg — Telegram user scan + history (Sangmata-style, local DB).

Usage:
  /sg                  → yourself
  /sg @username
  /sg <user_id>
  Reply to user + /sg
  Mention + /sg

Shows:
  • Full current TG profile (id, name, username, bio, DC, flags, photo)
  • History of name / username / bio / DP changes tracked by THIS bot

Note:
  Telegram official API does NOT give past change dates for arbitrary users.
  History builds when the bot sees the user in groups/DMs (auto tracker).
  Location history is not available via Telegram API for other users.
"""
import time
from datetime import datetime, timezone

from pyrogram import enums, filters, types
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied, UsernameInvalid

from TanuMusic import app, db, lang

# In-memory last snapshot to reduce DB writes
_LAST: dict[int, dict] = {}


def _ts() -> int:
    return int(time.time())


def _fmt_ts(ts: int | None) -> str:
    if not ts:
        return "—"
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).strftime(
            "%d %b %Y %H:%M UTC"
        )
    except Exception:
        return str(ts)


async def _resolve_user(m: types.Message):
    """Reply / mention / @user / id / self."""
    # 1) reply
    if m.reply_to_message and m.reply_to_message.from_user:
        return m.reply_to_message.from_user

    # 2) text mention entity
    if m.entities:
        for e in m.entities:
            if e.type == enums.MessageEntityType.TEXT_MENTION and e.user:
                return e.user

    # 3) argument
    if len(m.command) > 1:
        arg = m.command[1].strip()
        try:
            if arg.lstrip("-").isdigit():
                return await app.get_users(int(arg))
            return await app.get_users(arg)
        except (PeerIdInvalid, UsernameNotOccupied, UsernameInvalid, IndexError, KeyError, ValueError):
            return None
        except Exception:
            return None

    # 4) self
    return m.from_user


async def _get_full_chat(user_id: int):
    try:
        return await app.get_chat(user_id)
    except Exception:
        return None


async def track_user_snapshot(user: types.User, chat: types.Chat | None = None):
    """
    Compare with last known snapshot; if name/username/bio/photo changed,
    append to Mongo history.
    """
    if not user or user.is_bot:
        return

    uid = user.id
    full = await _get_full_chat(uid)
    bio = ""
    if full:
        bio = (getattr(full, "bio", None) or "")[:500]

    first = user.first_name or ""
    last = user.last_name or ""
    name = f"{first} {last}".strip()
    uname = (user.username or "").lower()
    photo_id = ""
    try:
        if user.photo:
            photo_id = str(getattr(user.photo, "big_file_id", None) or getattr(user.photo, "small_file_id", "") or "")
    except Exception:
        photo_id = ""

    snap = {
        "name": name,
        "username": uname,
        "bio": bio,
        "photo_id": photo_id,
        "ts": _ts(),
    }

    prev = _LAST.get(uid)
    if prev is None:
        # load from db once
        try:
            doc = await db.historydb.find_one({"_id": uid})
            if doc and doc.get("current"):
                prev = doc["current"]
                _LAST[uid] = prev
        except Exception:
            prev = None

    changes = []
    if prev:
        if prev.get("name") != snap["name"] and snap["name"]:
            changes.append({"type": "name", "old": prev.get("name"), "new": snap["name"], "ts": snap["ts"]})
        if prev.get("username") != snap["username"]:
            changes.append(
                {
                    "type": "username",
                    "old": prev.get("username") or None,
                    "new": snap["username"] or None,
                    "ts": snap["ts"],
                }
            )
        if prev.get("bio") != snap["bio"]:
            changes.append(
                {
                    "type": "bio",
                    "old": (prev.get("bio") or "")[:120],
                    "new": snap["bio"][:120],
                    "ts": snap["ts"],
                }
            )
        if prev.get("photo_id") != snap["photo_id"] and (snap["photo_id"] or prev.get("photo_id")):
            changes.append({"type": "photo", "old": bool(prev.get("photo_id")), "new": bool(snap["photo_id"]), "ts": snap["ts"]})

    try:
        update = {
            "$set": {
                "current": snap,
                "first_name": first,
                "last_name": last,
                "username": uname,
                "updated_at": snap["ts"],
            },
            "$setOnInsert": {"_id": uid, "created_at": snap["ts"]},
        }
        if changes:
            update["$push"] = {
                "history": {
                    "$each": changes,
                    "$slice": -100,  # keep last 100 events
                }
            }
        await db.historydb.update_one({"_id": uid}, update, upsert=True)
        _LAST[uid] = snap
    except Exception:
        pass


@app.on_message(filters.command(["sg", "history", "whois", "info"]) & ~app.bl_users)
@lang.language()
async def sg_cmd(_, m: types.Message):
    status = await m.reply_text("🔎 Scanning user...")

    user = await _resolve_user(m)
    if not user:
        return await status.edit_text(
            "❌ User not found.\n"
            "Use: <code>/sg @username</code> | <code>/sg user_id</code> | reply to user"
        )

    # Track snapshot on demand too
    await track_user_snapshot(user)

    full = await _get_full_chat(user.id)
    bio = getattr(full, "bio", None) or "None"
    dc = getattr(user, "dc_id", None) or getattr(full, "dc_id", None) or "Unknown"

    first = user.first_name or ""
    last = user.last_name or ""
    name = f"{first} {last}".strip() or "—"
    uname = f"@{user.username}" if user.username else "None"

    flags = []
    if user.is_bot:
        flags.append("Bot")
    if user.is_verified:
        flags.append("Verified")
    if user.is_premium:
        flags.append("Premium")
    if user.is_scam:
        flags.append("Scam")
    if user.is_fake:
        flags.append("Fake")
    if user.is_support:
        flags.append("Support")
    if getattr(user, "is_restricted", False):
        flags.append("Restricted")
    flag_txt = ", ".join(flags) if flags else "None"

    # Status / last online (if visible)
    status_txt = "Hidden / Unknown"
    try:
        st = user.status
        if st:
            sname = type(st).__name__
            if "Online" in sname:
                status_txt = "Online"
            elif "Offline" in sname:
                date = getattr(st, "date", None)
                status_txt = f"Offline ({_fmt_ts(int(date.timestamp()) if date else 0)})" if date else "Offline"
            elif "Recently" in sname:
                status_txt = "Last seen recently"
            elif "WithinWeek" in sname:
                status_txt = "Last seen within a week"
            elif "WithinMonth" in sname:
                status_txt = "Last seen within a month"
            elif "LongAgo" in sname:
                status_txt = "Last seen long ago"
            else:
                status_txt = sname
    except Exception:
        pass

    # History from DB
    hist_lines = []
    try:
        doc = await db.historydb.find_one({"_id": user.id})
        events = (doc or {}).get("history") or []
        # newest first
        events = list(reversed(events[-30:]))
        if not events:
            hist_lines.append("No change history yet (bot will track when it sees this user).")
        else:
            for ev in events:
                t = ev.get("type")
                when = _fmt_ts(ev.get("ts"))
                if t == "name":
                    hist_lines.append(f"• <b>Name</b> {_fmt_short(ev.get('old'))} → <code>{ev.get('new')}</code>\n  <i>{when}</i>")
                elif t == "username":
                    o = f"@{ev.get('old')}" if ev.get("old") else "None"
                    n = f"@{ev.get('new')}" if ev.get("new") else "None"
                    hist_lines.append(f"• <b>Username</b> {o} → {n}\n  <i>{when}</i>")
                elif t == "bio":
                    hist_lines.append(
                        f"• <b>Bio</b> changed\n  old: <code>{_esc(ev.get('old'))}</code>\n  new: <code>{_esc(ev.get('new'))}</code>\n  <i>{when}</i>"
                    )
                elif t == "photo":
                    hist_lines.append(f"• <b>DP / Photo</b> changed\n  <i>{when}</i>")
    except Exception as e:
        hist_lines.append(f"History load error: {e}")

    text = (
        f"🧬 <b>SG / User Scan</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"<b>Name:</b> {name}\n"
        f"<b>ID:</b> <code>{user.id}</code>\n"
        f"<b>Username:</b> {uname}\n"
        f"<b>Mention:</b> {user.mention}\n"
        f"<b>DC ID:</b> <code>{dc}</code>\n"
        f"<b>Status:</b> {status_txt}\n"
        f"<b>Flags:</b> {flag_txt}\n"
        f"<b>Bio:</b>\n<code>{_esc(bio)[:300]}</code>\n"
        f"━━━━━━━━━━━━━━\n"
        f"📜 <b>Change history</b> (tracked by this bot)\n"
        + ("\n".join(hist_lines) if hist_lines else "None")
        + "\n━━━━━━━━━━━━━━\n"
        f"ℹ️ <i>Location history is not provided by Telegram API.\n"
        f"Name/Username/Bio/DP history grows as bot sees the user in chats.</i>"
    )

    # Send with profile photo if any
    try:
        photos = []
        async for p in app.get_chat_photos(user.id, limit=1):
            photos.append(p)
        if photos:
            await status.delete()
            await m.reply_photo(photo=photos[0].file_id, caption=text)
            return
    except Exception:
        pass

    await status.edit_text(text)


def _esc(s) -> str:
    if s is None:
        return ""
    return str(s).replace("<", "<").replace(">", ">")


def _fmt_short(s) -> str:
    if not s:
        return "None"
    return f"<code>{_esc(s)}</code>"


# ---- Auto tracker: any incoming message from a user ----
@app.on_message(filters.incoming & filters.group & ~filters.service, group=90)
async def _sg_auto_track(_, m: types.Message):
    if not m.from_user or m.from_user.is_bot:
        return
    try:
        await track_user_snapshot(m.from_user)
    except Exception:
        pass


@app.on_message(filters.incoming & filters.private & ~filters.service, group=90)
async def _sg_auto_track_pm(_, m: types.Message):
    if not m.from_user or m.from_user.is_bot:
        return
    try:
        await track_user_snapshot(m.from_user)
    except Exception:
        pass
