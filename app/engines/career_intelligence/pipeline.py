"""
Career Intelligence Pipeline

This module orchestrates the complete AI Career Coach workflow.
"""

import logging

# ==========================================================
# Imports
# ==========================================================

from app.engines.matching.skill_extractor import extract_skills
from app.parsers.job_parser import extract_job_skills
from app.engines.matching.match_engine import calculate_match

# ATS
from app.engines.ats.ats_engine import analyze_resume

# Recommendation
from app.engines.career_intelligence.recommendation_engine import (
    RecommendationEngine
)

logger = logging.getLogger(__name__)


# ==========================================================
# Career Pipeline
# ==========================================================

class CareerPipeline:
    """
    Main orchestrator for AI Career Coach.
    """

    def __init__(self):

        # -----------------------------------------
        # Core Engines
        # -----------------------------------------

        self.skill_extractor = extract_skills

        self.job_parser = extract_job_skills

        self.match_engine = calculate_match

        # -----------------------------------------
        # ATS Engine
        # -----------------------------------------

        self.ats_engine = analyze_resume

        # -----------------------------------------
        # Recommendation Engine
        # -----------------------------------------

        self.recommendation_engine = RecommendationEngine()

    # ======================================================
    # Run Complete Pipeline
    # ======================================================

    def run(
        self,
        cv_text: str,
        job_description: str
    ) -> dict:

        logger.info("Starting career pipeline")

        # ==================================================
        # STEP 1
        # Extract CV Skills
        # ==================================================

        logger.info("Extracting CV skills")

        cv_skills = self.skill_extractor(cv_text)

        logger.debug("Found %d CV skills", len(cv_skills))

        # ==================================================
        # STEP 2
        # Extract Job Skills
        # ==================================================

        logger.info("Extracting job skills")

        job_skills = self.job_parser(job_description)

        logger.debug("Found %d job skills", len(job_skills))

        # ==================================================
        # STEP 3
        # Match Engine
        # ==================================================

        logger.info("Calculating match score")

        matched_skills, missing_skills, match_score = self.match_engine(
            cv_skills,
            job_skills
        )

        logger.info(
            "Match complete: matched=%d, missing=%d, score=%s",
            len(matched_skills),
            len(missing_skills),
            match_score,
        )

        # ==================================================
        # STEP 4
        # ATS Engine
        # ==================================================

        logger.info("Running ATS analysis")

        ats_result = self.ats_engine(
            cv_text,
            job_skills=job_skills
        )

        logger.info("ATS analysis complete")

        # ==================================================
        # STEP 5
        # Recommendation Engine
        # ==================================================

        logger.info("Generating recommendations")

        recommendations = self.recommendation_engine.generate(
            missing_skills
        )

        logger.info("Recommendations complete")

        # ==================================================
        # STEP 6
        # Final Report
        # ==================================================

        logger.info("Building final report")

        report = {

            "cv_skills": cv_skills,

            "job_skills": job_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "match_score": match_score,

            "ats": ats_result,

            "recommendations": recommendations

        }

        logger.info("Career pipeline finished successfully")

        return report
