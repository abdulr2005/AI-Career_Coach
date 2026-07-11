def build_roadmap(missing_skills):
    """
    Build a structured learning roadmap from missing skills.

    Args:
        missing_skills (list): List of skills user is missing.

    Returns:
        list: Structured roadmap steps.
    """

    # Knowledge base (can be moved later to DB or AI model)
    SKILL_INFO = {
        "Statistics": {
            "difficulty": "Beginner",
            "duration": "1 Week"
        },
        "Python": {
            "difficulty": "Beginner",
            "duration": "2 Weeks"
        },
        "SQL": {
            "difficulty": "Beginner",
            "duration": "1 Week"
        },
        "Machine Learning": {
            "difficulty": "Intermediate",
            "duration": "4 Weeks"
        },
        "Docker": {
            "difficulty": "Intermediate",
            "duration": "2 Weeks"
        },
        "Power BI": {
            "difficulty": "Beginner",
            "duration": "1 Week"
        },
        "Git": {
            "difficulty": "Beginner",
            "duration": "1 Week"
        }
    }

    roadmap = []

    step_number = 1

    for skill in missing_skills:
        if skill in SKILL_INFO:
            roadmap.append({
                "step": step_number,
                "skill": skill,
                "difficulty": SKILL_INFO[skill]["difficulty"],
                "duration": SKILL_INFO[skill]["duration"]
            })
            step_number += 1

    return roadmap