import re


# ==========================================
# Normalize Text
# ==========================================

def normalize_text(text: str) -> str:
    """
    Normalize resume text for consistent matching.

    Example:
    ----------
    PROFESSIONAL_SUMMARY
        -> professional summary

    Work-History
        -> work history

    Work   History
        -> work history
    """

    if not text:
        return ""

    text = text.lower()

    # Replace separators with spaces
    text = re.sub(r"[_\-/:]", " ", text)

    # Remove special characters
    text = re.sub(r"[^\w\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# Normalize Section Title
# ==========================================

def normalize_section_title(title: str) -> str:
    """
    Normalize section titles before matching.
    """

    return normalize_text(title)


# ==========================================
# Normalize Resume Lines
# ==========================================

def normalize_lines(lines: list[str]) -> list[str]:
    """
    Normalize every line in the resume.
    """

    return [
        normalize_text(line)
        for line in lines
        if line.strip()
    ]