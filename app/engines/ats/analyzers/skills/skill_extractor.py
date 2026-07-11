import re

# ==========================================================
# TECHNICAL SKILLS DATABASE
# ==========================================================

SKILL_KEYWORDS = [

    "python",
    "sql",
    "java",
    "c++",
    "javascript",

    "tensorflow",
    "pytorch",
    "scikit-learn",
    "opencv",

    "machine learning",
    "deep learning",
    "computer vision",
    "nlp",

    "xgboost",
    "random forest",
    "pca",

    "fastapi",
    "flask",
    "streamlit",

    "docker",
    "git",
    "github",

    "mysql",
    "postgresql",
    "mongodb",

    "power bi",
    "tableau",
    "excel",

    "aws",
    "azure",

    "iot",
    "uml",

    "react",
    "node.js",

    "linux",
    "kubernetes",

    "redis",

    "rest api",

    "api",

    "firebase",

    "azure devops"

]


# ==========================================================
# WORD BOUNDARY SEARCH
# ==========================================================

def contains_skill(text, skill):

    pattern = r"\b" + re.escape(skill) + r"\b"

    return re.search(pattern, text) is not None


# ==========================================================
# SKILL EXTRACTOR
# ==========================================================

def extract_skills_from_text(text):

    lower = text.lower()

    found = []

    for skill in SKILL_KEYWORDS:

        if contains_skill(lower, skill):

            found.append(skill)

    return sorted(set(found))