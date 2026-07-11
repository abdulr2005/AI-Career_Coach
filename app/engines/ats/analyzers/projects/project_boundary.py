import re


# ==========================================================
# DATE PATTERNS
# ==========================================================

DATE_PATTERNS = [

    r"\bPresent\b",
    r"\bCurrent\b",
    r"\b20\d{2}\b",
    r"\bJan\b|\bFeb\b|\bMar\b|\bApr\b|\bMay\b|\bJun\b|\bJul\b|\bAug\b|\bSep\b|\bOct\b|\bNov\b|\bDec\b",

]


# ==========================================================
# INVALID PROJECT STARTS
# ==========================================================

INVALID_STARTS = [

    "skills",
    "tools",
    "technology",
    "technologies",
    "responsibilities",
    "description",
    "summary",
    "github",
    "demo"

]


# ==========================================================
# IS PROJECT TITLE
# ==========================================================

def is_project_title(line: str):

    line = line.strip()

    if not line:
        return False

    lower = line.lower()

    # bullet line
    if line.startswith("•"):
        return False

    # description line
    if lower.startswith(tuple(INVALID_STARTS)):
        return False

    # too long
    if len(line) > 120:
        return False

    # has date
    if any(re.search(pattern, line) for pattern in DATE_PATTERNS):
        return True

    # title usually doesn't end with period
    if line.endswith("."):
        return False

    # short title
    words = len(line.split())

    if 2 <= words <= 12:
        return True

    return False