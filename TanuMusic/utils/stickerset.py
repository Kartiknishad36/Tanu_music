from typing import List

from pyrogram import Client
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.functions.stickers import CreateStickerSet, AddStickerToSet
from pyrogram.raw.types import InputStickerSetShortName, InputStickerSetItem, InputDocument


async def get_sticker_set_by_name(client: Client, name: str):
    try:
        return await client.invoke(
            GetStickerSet(stickerset=InputStickerSetShortName(short_name=name), hash=0)
        )
    except Exception:
        return None


async def create_sticker_set(client, owner_id, title, short_name, stickers):
    return await client.invoke(
        CreateStickerSet(
            user_id=await client.resolve_peer(owner_id),
            title=title,
            short_name=short_name,
            stickers=stickers,
            animated=False,
        )
    )
