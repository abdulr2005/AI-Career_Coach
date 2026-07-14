from .models import CareerReport


class CareerAnalyzer:

    def analyze(
        self,
        ats_score: float,
        match_score: float,
        extracted_skills: list,
        missing_skills: list,
    ) -> CareerReport:

        report = CareerReport(
            ats_score=ats_score,
            match_score=match_score,
            extracted_skills=extracted_skills,
            missing_skills=missing_skills,
        )

        return report