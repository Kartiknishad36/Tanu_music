n = "\n"
w = " "


bold = lambda x: f"**{x}:** "
bold_ul = lambda x: f"**--{x}:**-- "
mono = lambda x: f"`{x}`{n}"


def section(
    title: str,
    body: dict,
    indent: int = 2,
    underline: bool = False,
) -> str:
    section = [f"__{title}__:\n" if not underline else bold_ul(title)]
    for key, value in body.items():
        if value is None or value == "":
            continue
        section.append(
            f"{w * indent}{bold(key)}{value if not isinstance(value, list) else n.join(f'{w * 2 * indent}- {v}' for v in value)}\n"
        )
    return "".join(section)
