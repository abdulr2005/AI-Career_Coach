# ==========================================================
# REPORT BUILDER
# ==========================================================

def build_report(
    sections,
    skills,
    experience,
    projects,
    certifications,
    scores,
    summary
):

    report = {

        # -----------------------------------------
        # Original Resume Sections
        # -----------------------------------------

        "resume": {

            "summary": sections.get("summary", ""),

            "education": sections.get("education", ""),

            "experience": sections.get("experience", ""),

            "projects": sections.get("projects", ""),

            "skills": sections.get("skills", ""),

            "certifications": sections.get("certifications", "")

        },

        # -----------------------------------------
        # AI Analysis
        # -----------------------------------------

        "analysis": {

            "skills": skills,

            "experience": experience,

            "projects": projects,

            "certifications": certifications

        },

        # -----------------------------------------
        # Scores
        # -----------------------------------------

        "scores": scores,

        # -----------------------------------------
        # AI Summary
        # -----------------------------------------

        "strengths": summary["strengths"],

        "weaknesses": summary["weaknesses"],

        "recommendations": summary["recommendations"]

    }

    return report