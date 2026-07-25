from .models import (
    CareerReport,
    SkillGap,
    CourseRecommendation
)


class ReportGenerator:
    """
    Builds the final career report.
    """

    def generate(
        self,
        ats_score: float,
        match_score: float,
        extracted_skills: list,
        missing_skills: list,
        recommended_courses: list,
        roadmap: list,
        suggestions: list,
    ) -> CareerReport:

        gaps = [
            SkillGap(
                skill=skill["skill"],
                priority=skill["priority"]
            )
            for skill in missing_skills
        ]

        courses = [
            CourseRecommendation(
                title=course["title"],
                provider=course["provider"],
                url=course["url"]
            )
            for course in recommended_courses
        ]

        return CareerReport(
            ats_score=ats_score,
            match_score=match_score,
            extracted_skills=extracted_skills,
            missing_skills=gaps,
            recommended_courses=courses,
            roadmap=roadmap,
            suggestions=suggestions,
        )