COURSES = {

    "Python": {
        "course": "Python for Everybody",
        "provider": "Coursera"
    },

    "SQL": {
        "course": "SQL for Data Science",
        "provider": "Coursera"
    },

    "Power BI": {
        "course": "Microsoft Power BI Data Analyst",
        "provider": "Microsoft Learn"
    },

    "Excel": {
        "course": "Excel Skills for Business",
        "provider": "Coursera"
    },

    "Machine Learning": {
        "course": "Machine Learning Specialization",
        "provider": "Coursera"
    },

    "Deep Learning": {
        "course": "Deep Learning Specialization",
        "provider": "Coursera"
    },

    "TensorFlow": {
        "course": "TensorFlow Developer",
        "provider": "DeepLearning.AI"
    },

    "Pandas": {
        "course": "Data Analysis with Pandas",
        "provider": "freeCodeCamp"
    },

    "NumPy": {
        "course": "NumPy Course",
        "provider": "freeCodeCamp"
    },

    "Scikit-learn": {
        "course": "Machine Learning with Scikit-learn",
        "provider": "Kaggle Learn"
    },

    "Git": {
        "course": "Git & GitHub Crash Course",
        "provider": "freeCodeCamp"
    },

    "Docker": {
        "course": "Docker for Beginners",
        "provider": "KodeKloud"
    },

    "AWS": {
        "course": "AWS Cloud Practitioner Essentials",
        "provider": "AWS"
    },

    "Azure": {
        "course": "Microsoft Azure Fundamentals (AZ-900)",
        "provider": "Microsoft"
    },

    "GCP": {
        "course": "Google Cloud Digital Leader",
        "provider": "Google"
    },

    "R": {
        "course": "R Programming",
        "provider": "Coursera"
    },

    "Statistics": {
        "course": "Statistics with Python Specialization",
        "provider": "Coursera"
    }
}


def recommend_courses(missing_skills):
    """
    Recommend courses based on missing skills.

    Args:
        missing_skills (list): List of missing skills.

    Returns:
        list: Recommended courses.
    """

    recommendations = []

    for skill in missing_skills:

        if skill in COURSES:

            recommendations.append({
                "skill": skill,
                "course": COURSES[skill]["course"],
                "provider": COURSES[skill]["provider"]
            })

    return recommendations