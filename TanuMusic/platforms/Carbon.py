import random
from aiohttp import ClientSession, client_exceptions


class UnableToFetchCarbon(Exception):
    pass


themes = [
    "3024-night", "a11y-dark", "blackboard", "base16-dark", "dracula-pro",
    "material", "monokai", "nord", "one-dark", "synthwave-84", "vscode",
]
colour = [
    "#FF0000", "#FF5733", "#FFFF00", "#008000", "#0000FF", "#800080",
    "#00FFFF", "#FF00FF", "#000000", "#FFFFFF",
]


class CarbonAPI:
    def __init__(self):
        self.language = "auto"
        self.drop_shadow = True
        self.drop_shadow_blur = "68px"
        self.drop_shadow_offset = "20px"
        self.font_family = "JetBrains Mono"
        self.width_adjustment = True
        self.watermark = False

    async def generate(self, text: str, user_id):
        async with ClientSession(headers={"Content-Type": "application/json"}) as ses:
            params = {
                "code": text,
                "backgroundColor": random.choice(colour),
                "theme": random.choice(themes),
                "dropShadow": self.drop_shadow,
                "dropShadowOffsetY": self.drop_shadow_offset,
                "dropShadowBlurRadius": self.drop_shadow_blur,
                "fontFamily": self.font_family,
                "language": self.language,
                "watermark": self.watermark,
                "widthAdjustment": self.width_adjustment,
            }
            try:
                request = await ses.post(
                    "https://carbonara.solopov.dev/api/cook", json=params
                )
            except client_exceptions.ClientConnectorError:
                raise UnableToFetchCarbon("Can not reach the Host!")
            resp = await request.read()
            with open(f"cache/carbon{user_id}.jpg", "wb") as f:
                f.write(resp)
            return f"cache/carbon{user_id}.jpg"
