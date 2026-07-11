def generate_suggestions(missing_skills):

    suggestions = []

    for skill in missing_skills:

        suggestions.append(
            f"Consider learning {skill} to improve your chances."
        )

    return suggestions