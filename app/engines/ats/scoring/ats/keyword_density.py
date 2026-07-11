from collections import Counter
import re


# ==================================================
# CLEAN TEXT
# ==================================================

def normalize(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


# ==================================================
# KEYWORD DENSITY
# ==================================================

def analyze_keyword_density(cv_text, job_skills):

    cv_text = normalize(cv_text)

    words = cv_text.split()

    counter = Counter(words)

    density = {}

    total = len(words)

    if total == 0:
        total = 1

    for skill in job_skills:

        key = skill.lower()

        count = cv_text.count(key)

        density[skill] = {

            "count": count,

            "density": round((count / total) * 100, 2)

        }

    return density