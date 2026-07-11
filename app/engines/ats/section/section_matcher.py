from app.data.resume_patterns import SECTION_PATTERNS
from app.engines.ats.section.normalizer import normalize_section_title


# ==========================================
# Match Resume Section
# ==========================================

def match_section(title: str) -> str | None:
    """
    Convert any resume heading into
    one standard section name.

    Example
    -------
    PROFESSIONAL SUMMARY
        -> summary

    Work Experience
        -> experience

    Technical Projects
        -> projects
    """

    normalized = normalize_section_title(title)

    for section_name, patterns in SECTION_PATTERNS.items():

        normalized_patterns = [

            normalize_section_title(pattern)

            for pattern in patterns

        ]

        if normalized in normalized_patterns:

            return section_name

    return None


# ==========================================
# Check if Line is Section
# ==========================================

def is_section(line: str) -> bool:

    return match_section(line) is not None


# ==========================================
# Get Canonical Name
# ==========================================

def canonical_section(line: str) -> str:

    result = match_section(line)

    if result:

        return result

    return "other"