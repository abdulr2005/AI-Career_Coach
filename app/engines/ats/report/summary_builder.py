def build_summary(
    scores,
    skills,
    experience,
    projects,
    certifications
):

    strengths = []

    weaknesses = []

    recommendations = []

    # -------------------------
    # Skills
    # -------------------------

    if len(skills) >= 10:

        strengths.append(
            "Strong technical skill set."
        )

    else:

        weaknesses.append(
            "Limited technical skills."
        )

        recommendations.append(
            "Add more job-related technical skills."
        )

    # -------------------------
    # Projects
    # -------------------------

    if projects["average_score"] >= 8:

        strengths.append(
            "High-quality projects with measurable impact."
        )

    else:

        recommendations.append(
            "Improve project descriptions using metrics."
        )

    # -------------------------
    # Experience
    # -------------------------

    if experience["count"] == 0:

        weaknesses.append(
            "No work experience detected."
        )

        recommendations.append(
            "Add internships, volunteering or freelance work."
        )

    # -------------------------
    # Certifications
    # -------------------------

    if certifications["count"] == 0:

        recommendations.append(
            "Consider adding professional certifications."
        )

    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations

    }