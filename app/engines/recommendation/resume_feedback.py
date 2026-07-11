def generate_resume_feedback(matched_skills, missing_skills):
    """
    Generate feedback for improving the CV.
    """

    feedback = []

    # Positive Feedback
    if len(matched_skills) > 0:
        feedback.append(
            f"Great! Your CV already matches {len(matched_skills)} required skills."
        )

    # Missing Skills
    for skill in missing_skills:
        feedback.append(
            f"Consider learning {skill} and adding projects that demonstrate it."
        )

    # General Tips
    feedback.append("Add strong projects to your CV.")
    feedback.append("Include certifications related to your field.")
    feedback.append("Keep your GitHub portfolio updated.")
    feedback.append("Quantify your achievements with numbers whenever possible.")

    return feedback