"""
Career Recommendation Engine

This module combines all recommendation engines
into one interface for the Career Pipeline.
"""

import logging

# ==========================================================
# Imports
# ==========================================================

from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions

logger = logging.getLogger(__name__)


# ==========================================================
# Recommendation Engine
# ==========================================================

class RecommendationEngine:
    """
    Wrapper around all recommendation modules.
    """

    def generate(self, missing_skills):

        logger.info("Generating recommendations")

        # ------------------------------------------
        # Courses
        # ------------------------------------------

        courses = recommend_courses(
            missing_skills
        )

        logger.info("Courses generated")

        # ------------------------------------------
        # Roadmap
        # ------------------------------------------

        roadmap = build_roadmap(
            missing_skills
        )

        logger.info("Roadmap generated")

        # ------------------------------------------
        # Suggestions
        # ------------------------------------------

        suggestions = generate_suggestions(
            missing_skills
        )

        logger.info("Suggestions generated")

        return {

            "courses": courses,

            "roadmap": roadmap,

            "suggestions": suggestions

        }
