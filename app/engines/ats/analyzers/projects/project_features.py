import re

from app.data.project_patterns import (
    ACTION_VERBS,
    IMPACT_WORDS,
    TEAMWORK_WORDS,
    ACHIEVEMENT_WORDS,
    LINK_WORDS
)


# ==========================================================
# ACTION VERBS
# ==========================================================

def extract_action_verbs(text):

    lower = text.lower()

    return sorted({

        word

        for word in ACTION_VERBS

        if word in lower

    })


# ==========================================================
# IMPACT WORDS
# ==========================================================

def extract_impact(text):

    lower = text.lower()

    return sorted({

        word

        for word in IMPACT_WORDS

        if word in lower

    })


# ==========================================================
# TEAMWORK
# ==========================================================

def detect_teamwork(text):

    lower = text.lower()

    return any(

        word in lower

        for word in TEAMWORK_WORDS

    )


# ==========================================================
# ACHIEVEMENTS
# ==========================================================

def extract_achievements(text):

    lower = text.lower()

    return sorted({

        word

        for word in ACHIEVEMENT_WORDS

        if word in lower

    })


# ==========================================================
# LINKS
# ==========================================================

def detect_links(text):

    lower = text.lower()

    return {

        "github": "github" in lower,

        "portfolio": "portfolio" in lower,

        "demo": any(

            word in lower

            for word in LINK_WORDS

        )

    }


# ==========================================================
# METRICS
# ==========================================================

def extract_metrics(text):

    metrics = []

    patterns = [

        r"\d+(?:\.\d+)?%",             # 92.4%

        r"\d+(?:\.\d+)?[KMB]",         # 100K / 1M / 2B

        r"\d+x",                       # 2x

        r"\d+\s?(?:GB|MB|TB)",         # 5GB

        r"\d+\s?(?:ms|sec|seconds)",   # 120ms

        r"\d+\s?(?:users|records)",    # 1M records

        r"\d+\+"                       # 100+

    ]

    for pattern in patterns:

        metrics.extend(re.findall(pattern, text, re.IGNORECASE))

    return sorted(set(metrics))