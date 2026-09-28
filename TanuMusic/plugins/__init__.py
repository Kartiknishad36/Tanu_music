# ===============================================================================
# __init__.py - Plugin Auto-Discovery
# ===============================================================================
from pathlib import Path

def _list_modules():
    mod_dir = Path(__file__).parent
    modules = []

    for file in mod_dir.rglob("*.py"):
        if file.is_file() and file.name != "__init__.py":
            relative_path = file.relative_to(mod_dir)
            module_path = str(relative_path.with_suffix(
                '')).replace('\\', '.').replace('/', '.')
            modules.append(module_path)

    return modules


all_modules = frozenset(sorted(_list_modules()))
