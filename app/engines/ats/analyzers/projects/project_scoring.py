from app.engines.ats.analyzers.projects.project_features import (
    extract_action_verbs,
    extract_impact,
    extract_metrics,
    extract_achievements,
    detect_teamwork,
    detect_links
)

from app.engines.ats.analyzers.skills.skill_extractor import (
    extract_skills_from_text
)


# ==========================================================
# SCORE SINGLE PROJECT
# ==========================================================

def score_project(project_text):

    skills = extract_skills_from_text(project_text)

    verbs = extract_action_verbs(project_text)

    metrics = extract_metrics(project_text)

    achievements = extract_achievements(project_text)

    impacts = extract_impact(project_text)

    teamwork = detect_teamwork(project_text)

    links = detect_links(project_text)

    score = 0

    # Skills
    score += min(len(skills), 10)

    # Action verbs
    score += min(len(verbs), 5)

    # Metrics
    score += min(len(metrics), 5)

    # Achievements
    score += len(achievements) * 2

    # Impact
    score += min(len(impacts), 5)

    # Teamwork
    if teamwork:
        score += 2

    # GitHub / Demo
    if links["github"]:
        score += 2

    if links["portfolio"]:
        score += 2

    if links["demo"]:
        score += 1

    score = min(score, 30)

    return {

        "score": score,

        "skills": skills,

        "action_verbs": verbs,

        "metrics": metrics,

        "achievements": achievements,

        "impact": impacts,

        "teamwork": teamwork,

        "links": links

    }


# ==========================================================
# SCORE ALL PROJECTS
# ==========================================================

def score_projects(projects):

    results = []

    total_score = 0

    for project in projects:

        result = score_project(project)

        results.append(result)

        total_score += result["score"]

    average = 0

    if results:
        average = round(total_score / len(results), 2)

    return {

        "projects": results,

        "project_count": len(results),

        "average_score": average,

        "total_score": total_score

    }