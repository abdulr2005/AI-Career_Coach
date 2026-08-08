import re

from app.data.skills_db import TECHNICAL_KEYWORDS


# ==================================================
# TECHNOLOGY KEYWORDS
# ==================================================


# ==================================================
# METRIC PATTERNS
# ==================================================

METRIC_PATTERNS = [

    r"\d+(\.\d+)?%",
    r"\d+\s*million",
    r"\d+\s*k",
    r"\d+\+",
    r"\d+\s*records",
    r"\d+\s*users"

]


# ==================================================
# EXTRACT TECHNOLOGIES
# ==================================================

def extract_technologies(text):

    lower = text.lower()

    found = []

    for tech in TECHNICAL_KEYWORDS:

        if tech in lower:
            found.append(tech)

    return sorted(list(set(found)))


# ==================================================
# EXTRACT METRICS
# ==================================================

def extract_metrics(text):

    metrics = []

    for pattern in METRIC_PATTERNS:

        metrics.extend(

            re.findall(

                pattern,

                text,

                flags=re.IGNORECASE

            )

        )

    return metrics


# ==================================================
# ANALYZE PROJECTS
# ==================================================

def analyze_projects(project_text):

    if isinstance(project_text, list):

        project_text = "\n".join(project_text)

    technologies = extract_technologies(project_text)

    metrics = extract_metrics(project_text)

    github = "github" in project_text.lower()

    demo = any(

        word in project_text.lower()

        for word in [

            "demo",

            "live",

            "website",

            "streamlit"

        ]

    )

    ai_project = any(

        word in project_text.lower()

        for word in [

            "machine learning",

            "deep learning",

            "ai",

            "computer vision",

            "nlp"

        ]

    )

    score = 0

    score += min(len(technologies), 5)

    score += min(len(metrics), 2)

    if github:
        score += 1

    if demo:
        score += 1

    if ai_project:
        score += 1

    score = min(score, 10)

    return {

        "technologies": technologies,

        "technology_count": len(technologies),

        "metrics": metrics,

        "github_found": github,

        "demo_found": demo,

        "ai_project": ai_project,

        "score": score

    }
