import logging

from app.engines.ats.section.section_utils import (
    split_resume,
    clean_lines
)

from app.engines.ats.section.section_matcher import (
    match_section
)

logger = logging.getLogger(__name__)


# ==========================================
# Resume Section Parser V2
# ==========================================

def parse_resume_sections(text: str):

    lines = split_resume(text)

    lines = clean_lines(lines)

    sections = {}

    current_section = "other"

    sections[current_section] = []

    for line in lines:

        section = match_section(line)

        if section:

            current_section = section

            if current_section not in sections:

                sections[current_section] = []

            continue

        sections[current_section].append(line)

    # Convert lists to strings

    final_sections = {}

    for key, value in sections.items():

        final_sections[key] = "\n".join(value).strip()

    return final_sections
