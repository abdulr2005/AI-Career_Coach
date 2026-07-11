# ==================================================
# SKILL GAP ANALYZER
# ==================================================

def analyze_skill_gap(cv_skills, job_skills):

    cv = {skill.lower().strip() for skill in cv_skills}
    job = {skill.lower().strip() for skill in job_skills}

    matched = sorted(list(cv & job))
    missing = sorted(list(job - cv))
    extra = sorted(list(cv - job))

    if len(job) == 0:
        coverage = 100.0
    else:
        coverage = round((len(matched) / len(job)) * 100, 2)

    # ==============================================
    # Priority Classification
    # ==============================================

    critical = []
    preferred = []

    for skill in missing:

        if skill in [
            "python",
            "sql",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "aws",
            "azure",
            "docker",
            "fastapi"
        ]:
            critical.append(skill)
        else:
            preferred.append(skill)

    return {

        "matched": matched,

        "missing": missing,

        "extra": extra,

        "coverage": coverage,

        "critical_missing": critical,

        "preferred_missing": preferred

    }