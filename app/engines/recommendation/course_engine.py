from app.data.courses_db import COURSES


def recommend_courses(missing_skills):
    """
    Recommend courses based on missing skills.

    Args:
        missing_skills (list): List of missing skills.

    Returns:
        list: Recommended courses.
    """

    recommendations = []

    for skill in missing_skills:

        if skill in COURSES:

            recommendations.append({
                "skill": skill,
                "course": COURSES[skill]["course"],
                "provider": COURSES[skill]["provider"]
            })

    return recommendations
