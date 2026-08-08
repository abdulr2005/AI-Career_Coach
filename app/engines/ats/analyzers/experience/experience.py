import re

from app.data.skills_db import TECHNICAL_KEYWORDS


# ==================================================
# ACTION VERBS
# ==================================================

ACTION_VERBS = [

    "developed",
    "built",
    "created",
    "designed",
    "implemented",
    "optimized",
    "improved",
    "achieved",
    "reduced",
    "increased",
    "managed",
    "led",
    "trained",
    "engineered",
    "automated",
    "deployed"

]


# ==================================================
# LEADERSHIP WORDS
# ==================================================

LEADERSHIP_WORDS = [

    "lead",
    "leader",
    "managed",
    "supervised",
    "mentored",
    "headed",
    "organized"

]


# ==================================================
# INTERNSHIP WORDS
# ==================================================

INTERNSHIP_WORDS = [

    "intern",
    "internship",
    "trainee",
    "training",
    "co-op"

]


# ==================================================
# EXTRACT TECHNOLOGIES
# ==================================================

def extract_technologies(text):

    lower = text.lower()

    return sorted({

        tech

        for tech in TECHNICAL_KEYWORDS

        if tech in lower

    })


# ==================================================
# ACTION VERBS
# ==================================================

def extract_action_verbs(text):

    lower = text.lower()

    return [

        word

        for word in ACTION_VERBS

        if word in lower

    ]


# ==================================================
# METRICS
# ==================================================

def extract_metrics(text):

    return re.findall(

        r"\d+(?:\.\d+)?%?|\d+[kKmM]?",

        text

    )


# ==================================================
# YEARS
# ==================================================

def extract_years(text):

    years = re.findall(

        r"(20\d{2})",

        text

    )

    return sorted(set(years))


# ==================================================
# EXPERIENCE ANALYZER
# ==================================================

def analyze_experience(text):

    lower = text.lower()

    technologies = extract_technologies(text)

    actions = extract_action_verbs(text)

    metrics = extract_metrics(text)

    years = extract_years(text)

    internship = any(

        word in lower

        for word in INTERNSHIP_WORDS

    )

    leadership = any(

        word in lower

        for word in LEADERSHIP_WORDS

    )

    score = 0

    score += min(len(technologies), 10) * 0.4
    score += min(len(actions), 10) * 0.3
    score += min(len(metrics), 10) * 0.2

    if internship:
        score += 1

    if leadership:
        score += 1

    score = min(round(score, 2), 10)

    if score >= 8:
        impact = "High"
    elif score >= 5:
        impact = "Medium"
    else:
        impact = "Low"

    return {

        "score": score,

        "impact": impact,

        "technologies": technologies,

        "technology_count": len(technologies),

        "action_verbs": actions,

        "action_count": len(actions),

        "metrics": metrics,

        "metrics_count": len(metrics),

        "years": years,

        "leadership": leadership,

        "internship": internship

    }
