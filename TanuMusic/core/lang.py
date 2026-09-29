import json
from functools import wraps
from pathlib import Path

from TanuMusic import logger

lang_codes = {
    "en": "🇺🇸 English",
    "si": "🇱🇰 සිංහල",
    "ta": "🇮🇳 தமிழ்",
    "hi": "🇮🇳 हिन्दी",
    "ms": "🇲🇾 Bahasa Melayu",
    "tl": "🇵🇭 Filipino",
    "ru": "🇷🇺 Русский",
}


class LangDict(dict):
    def __init__(self, primary_dict, fallback_dict):
        super().__init__(primary_dict)
        self.fallback = fallback_dict

    def __getitem__(self, key):
        try:
            val = super().__getitem__(key)
            if not val:
                return self.fallback.get(key, key)
            return val
        except KeyError:
            return self.fallback.get(key, key)


class Language:
    def __init__(self):
        self.lang_codes = lang_codes
        self.lang_dir = Path("TanuMusic/locales")
        self.languages = self.load_files()

    def load_files(self):
        languages = {}
        for lang_code in self.lang_codes.keys():
            lang_file = self.lang_dir / f"{lang_code}.json"
            if lang_file.exists():
                try:
                    with open(lang_file, "r", encoding="utf-8") as file:
                        languages[lang_code] = json.load(file)
                except Exception as e:
                    logger.error(f"Failed to load language {lang_code}: {e}")
            else:
                logger.warning(f"Language file not found: {lang_file}")

        if "en" not in languages:
            languages["en"] = {}

        logger.info(f"Loaded languages: {', '.join(languages.keys())}")
        return languages

    async def get_lang(self, chat_id: int) -> dict:
        import TanuMusic

        db = TanuMusic.db
        lang_code = "en"
        if db is not None:
            try:
                lang_code = await db.get_lang(chat_id)
            except Exception:
                lang_code = "en"
        if lang_code not in self.languages:
            lang_code = "en"

        if lang_code == "en":
            return self.languages["en"]

        return LangDict(self.languages[lang_code], self.languages["en"])

    def language(self):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                import TanuMusic

                db = TanuMusic.db

                fallen = next(
                    (
                        arg
                        for arg in args
                        if hasattr(arg, "chat") or hasattr(arg, "message")
                    ),
                    None,
                )

                if hasattr(fallen, "chat"):
                    chat = fallen.chat
                elif hasattr(fallen, "message"):
                    chat = fallen.message.chat
                else:
                    return await func(*args, **kwargs)

                # Safe blacklist check — never crash if db not ready
                try:
                    bl = getattr(db, "blacklisted", None) if db is not None else None
                    if bl is not None and chat.id in bl:
                        try:
                            return await chat.leave()
                        except Exception:
                            return
                except Exception:
                    pass

                lang_code = "en"
                if db is not None:
                    try:
                        lang_code = await db.get_lang(chat.id)
                    except Exception:
                        lang_code = "en"
                if lang_code not in self.languages:
                    lang_code = "en"

                if lang_code == "en":
                    lang_dict = self.languages["en"]
                else:
                    lang_dict = LangDict(
                        self.languages.get(lang_code, {}),
                        self.languages["en"],
                    )

                setattr(fallen, "lang", lang_dict)
                return await func(*args, **kwargs)

            return wrapper

        return decorator
