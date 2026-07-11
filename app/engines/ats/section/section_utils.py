import re


# ==========================================
# Split Resume into Lines
# ==========================================

def split_resume(text: str) -> list[str]:
    """
    Split resume into clean lines.
    """

    if not text:
        return []

    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


# ==========================================
# Remove Empty Lines
# ==========================================

def remove_empty_lines(lines: list[str]) -> list[str]:

    return [
        line
        for line in lines
        if line.strip()
    ]


# ==========================================
# Remove Duplicate Spaces
# ==========================================

def remove_duplicate_spaces(text: str) -> str:

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


# ==========================================
# Clean Resume Lines
# ==========================================

def clean_lines(lines: list[str]) -> list[str]:

    cleaned = []

    for line in lines:

        line = remove_duplicate_spaces(line)

        if line:

            cleaned.append(line)

    return cleaned


# ==========================================
# Merge Lines
# ==========================================

def merge_lines(lines: list[str]) -> str:

    return "\n".join(lines)


# ==========================================
# Is Empty Line
# ==========================================

def is_empty_line(line: str) -> bool:

    return len(line.strip()) == 0


# ==========================================
# Is Bullet Point
# ==========================================

def is_bullet(line: str) -> bool:

    bullets = (
        "•",
        "-",
        "*",
        "▪",
        "◦",
        "○"
    )

    return line.strip().startswith(bullets)


# ==========================================
# Resume Statistics
# ==========================================

def resume_statistics(text: str):

    words = len(text.split())

    chars = len(text)

    lines = len(text.splitlines())

    return {

        "words": words,

        "characters": chars,

        "lines": lines

    }