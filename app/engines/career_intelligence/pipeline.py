"""
Career Intelligence Pipeline

This module orchestrates the complete AI Career Coach workflow.
"""

# ==========================================================
# Imports
# ==========================================================

from app.engines.matching.skill_extractor import extract_skills
from app.parsers.job_parser import extract_job_skills
from app.engines.matching.match_engine import calculate_match


# ==========================================================
# Career Pipeline
# ==========================================================

class CareerPipeline:
    """
    Main orchestrator for AI Career Coach.
    """

    def __init__(self):

        # -----------------------------------------
        # Register all engines
        # -----------------------------------------

        self.skill_extractor = extract_skills
        self.job_parser = extract_job_skills
        self.match_engine = calculate_match

        # These will be connected later

        self.ats_engine = None
        self.recommendation_engine = None
        self.report_generator = None

    # ======================================================
    # Run Complete Pipeline
    # ======================================================

    def run(
        self,
        cv_text: str,
        job_description: str
    ) -> dict:

        print("\n========== Career Pipeline ==========")

        # ==================================================
        # STEP 1
        # Extract CV Skills
        # ==================================================

        print("\n[1] Extracting CV Skills...")

        cv_skills = self.skill_extractor(cv_text)

        print(f"Found {len(cv_skills)} skills")
        print(cv_skills)

        # ==================================================
        # STEP 2
        # Extract Job Skills
        # ==================================================

        print("\n[2] Extracting Job Skills...")

        job_skills = self.job_parser(job_description)

        print(f"Found {len(job_skills)} job skills")
        print(job_skills)

        # ==================================================
        # STEP 3
        # Match Engine
        # ==================================================

        print("\n[3] Calculating Match Score...")

        matched_skills, missing_skills, match_score = self.match_engine(
            cv_skills,
            job_skills
        )

        print("Match Finished")

        print(f"Matched Skills : {len(matched_skills)}")
        print(f"Missing Skills : {len(missing_skills)}")
        print(f"Match Score    : {match_score}")

        # ==================================================
        # STEP 4
        # ATS
        # ==================================================

        print("\n[4] ATS Engine")

        ats_result = None

        print("ATS Engine not connected yet.")

        # ==================================================
        # STEP 5
        # Recommendation
        # ==================================================

        print("\n[5] Recommendation Engine")

        recommendations = None

        print("Recommendation Engine not connected yet.")

        # ==================================================
        # STEP 6
        # Final Report
        # ==================================================

        print("\n[6] Building Report...")

        report = {

            "cv_skills": cv_skills,

            "job_skills": job_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_score": match_score,

            "ats": ats_result,

            "recommendations": recommendations

        }

        print("Pipeline Finished Successfully")

        return report