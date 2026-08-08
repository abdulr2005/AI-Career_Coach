from app.data.roadmap_db import ROADMAP_SKILLS


def build_roadmap(missing_skills):
    """
    Build a structured learning roadmap from missing skills.

    Args:
        missing_skills (list): List of skills user is missing.

    Returns:
        list: Structured roadmap steps.
    """

    roadmap = []

    step_number = 1

    for skill in missing_skills:
        if skill in ROADMAP_SKILLS:
            roadmap.append({
                "step": step_number,
                "skill": skill,
                "difficulty": ROADMAP_SKILLS[skill]["difficulty"],
                "duration": ROADMAP_SKILLS[skill]["duration"]
            })
            step_number += 1

    return roadmap
