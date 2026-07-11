# ==================================================
# RESUME QUALITY ANALYZER
# ==================================================

def analyze_resume_quality(

    ats_score,
    experience,
    projects,
    certifications

):

    feedback = []

    strengths = []

    weaknesses = []

    # ==========================================
    # Overall ATS Score
    # ==========================================

    if ats_score >= 90:

        level = "Excellent"

        feedback.append(
            "Your resume is highly optimized for ATS systems."
        )

    elif ats_score >= 75:

        level = "Good"

        feedback.append(
            "Your resume is ATS-friendly but still has room for improvement."
        )

    elif ats_score >= 60:

        level = "Average"

        feedback.append(
            "Your resume passes many ATS checks but should be improved."
        )

    else:

        level = "Poor"

        feedback.append(
            "Your resume is unlikely to perform well in ATS systems."
        )

    # ==========================================
    # Experience
    # ==========================================

    if experience["score"] >= 7:

        strengths.append(
            "Strong technical project experience."
        )

    else:

        weaknesses.append(
            "Add more technical projects or work experience."
        )

    # ==========================================
    # Projects
    # ==========================================

    if projects["score"] >= 7:

        strengths.append(
            "Projects demonstrate solid technical skills."
        )

    else:

        weaknesses.append(
            "Improve your projects by adding measurable impact and GitHub links."
        )

    # ==========================================
    # Certifications
    # ==========================================

    if certifications["score"] >= 5:

        strengths.append(
            "Good collection of professional certifications."
        )

    else:

        weaknesses.append(
            "Consider earning certifications from Microsoft, AWS, Cisco, or Google."
        )

    # ==========================================
    # Final Recommendation
    # ==========================================

    recommendation = []

    if ats_score < 90:

        recommendation.append(
            "Improve keyword matching with the target job description."
        )

        recommendation.append(
            "Use more quantified achievements in projects."
        )

        recommendation.append(
            "Include additional industry-recognized certifications."
        )

        recommendation.append(
            "Expand your technical experience section."
        )

    # ==========================================

    return {

        "level": level,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "feedback": feedback,

        "recommendation": recommendation

    }