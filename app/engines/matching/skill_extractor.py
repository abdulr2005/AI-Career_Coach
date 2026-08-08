import re

from app.data.skills_db import SKILLS_DB


def normalize_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", " ", text)

    return text


def extract_skills(text):

    text = normalize_text(text)

    found_skills = []

    for skill in SKILLS_DB:

        normalized_skill = normalize_text(skill)

        if normalized_skill in text:

            found_skills.append(skill)

    return found_skills
