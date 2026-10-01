# Original Tanu Music plugins only (ignore leftover BABY folders)
from pathlib import Path

# Only these folders are original Tanu Music
_ALLOWED = {
    "admin",
    "events",
    "games",
    "info",
    "playback",
    "settings",
    "utilities",
}


def _list_modules():
    mod_dir = Path(__file__).parent
    modules = []
    for file in mod_dir.rglob("*.py"):
        if not file.is_file() or file.name == "__init__.py":
            continue
        relative_path = file.relative_to(mod_dir)
        parts = relative_path.parts
        if not parts or parts[0] not in _ALLOWED:
            continue
        module_path = str(relative_path.with_suffix("")).replace("\\", ".").replace("/", ".")
        modules.append(module_path)
    return modules


all_modules = frozenset(sorted(_list_modules()))
