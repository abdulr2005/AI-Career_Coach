import re

from app.data.resume_patterns import SECTION_PATTERNS


def parse_resume_sections(cv_text):

    sections = {}

    lines = cv_text.splitlines()

    current_section = "other"

    sections[current_section] = []

    for line in lines:

        clean = line.strip()

        if not clean:
            continue

        found = False

        for section, titles in SECTION_PATTERNS.items():

            if clean.lower() in [t.lower() for t in titles]:

                current_section = section

                sections[current_section] = []

                found = True

                break

        if not found:

            sections[current_section].append(clean)

    return sections
