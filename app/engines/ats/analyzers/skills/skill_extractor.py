import re

from app.data.skills_db import ATS_SKILL_KEYWORDS


def contains_skill(text, skill):

    pattern = r"\b" + re.escape(skill) + r"\b"

    return re.search(pattern, text) is not None


def extract_skills_from_text(text):

    lower = text.lower()

    found = []

    for skill in ATS_SKILL_KEYWORDS:

        if contains_skill(lower, skill):

            found.append(skill)

    return sorted(set(found))
