from rapidfuzz import fuzz


def calculate_match(cv_skills, job_skills):

    matched_skills = []

    missing_skills = []

    for job_skill in job_skills:

        found = False

        for cv_skill in cv_skills:

            similarity = fuzz.ratio(
                cv_skill.lower(),
                job_skill.lower()
            )

            if similarity >= 85:

                matched_skills.append(job_skill)

                found = True

                break

        if not found:

            missing_skills.append(job_skill)

    if len(job_skills) == 0:

        match_score = 0

    else:

        match_score = round(
            len(matched_skills) / len(job_skills) * 100,
            2
        )

    return matched_skills, missing_skills, match_score