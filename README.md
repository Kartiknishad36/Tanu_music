# 🎵 Tanu Music

Full-featured Telegram Music + Tools bot (BABYXMUSIC-style), rebranded for **Tanu Music**.

**Owner:** [@KARTIK_NISHAD_3](https://t.me/KARTIK_NISHAD_3)  
**Support:** https://t.me/+M5ApQJTxdxgxMDg1  
**Channel:** https://t.me/ye_duniya_ek_sapna_he  

## Deploy (Railway)

1. New project → Deploy from GitHub (`Kartiknishad36/Tanu_music`)
2. Set variables from `sample.env`
3. Required:
   - `API_ID` `API_HASH` `BOT_TOKEN`
   - `STRING_SESSION` (Pyrogram user session for assistant/VC)
   - `MONGO_DB_URI`
   - `LOGGER_ID` (log group id, bot must be admin)
   - `OWNER_ID`
4. Optional: `COOKIE_URL` (pastebin raw YouTube cookies)

## Run locally

```bash
pip install -r requirements.txt
# fill .env
bash start
```

## Features (same family as BABYXMUSIC)

- Music VC: `/play` `/vplay` `/pause` `/resume` `/skip` `/stop` `/queue`
- Multi-assistant sessions (`STRING_SESSION` … `STRING_SESSION7`)
- Admin tools, tags, ban/mute, broadcast
- Tools: song download, ping, stats, AFK, couples, stickers, translate, …
- Sudo / gban / maintenance
- Yumi extras: weather, QR, fonts, games, …

Package name: `TanuMusic` (`python3 -m TanuMusic`)
